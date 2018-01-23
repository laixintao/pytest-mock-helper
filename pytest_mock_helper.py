# -*- coding: utf-8 -*-

"""
Hook ``requests.adapters.HTTPAdapter.send``
"""

import os

from urllib.parse import urlparse
import requests
import logging
from collections import namedtuple


logger = logging.getLogger(__name__)

is_develop = os.getenv("PYTEST_NETWORK_MOCK", "product") == "develop"
file_save_path = os.getenv("PYTEST_NETWORK_FILEPATH")
template_path = os.getenv("PYTEST_NETOWRK_TEMPLATE")
template = """
@httmock.urlmatch(netloc="{0.netloc}", path="{0.path}")
def mock_item(url, request):
    return test_utils.fake_response(
        rel_path="{0.filename}",
        url="{0.request.url}",
        status_code=200
    )
"""

if template_path:
    with open(template_path) as template_file:
        template = template_file.read()

summaries = []
Mock = namedtuple("Mock", "filename netloc path request")


class MockHttpCall(Exception):
    """Please mock http call"""


def block_http(whitelist):
    def whitelisted(self, request, *args, **kwargs):
        global summaries
        parsed = urlparse(request.url)
        netloc = parsed.netloc
        path = parsed.path
        if isinstance(netloc, str) and netloc in whitelist:
            return self.old_send(request, *args, **kwargs)

        if not is_develop:
            logger.warning('Denied HTTP connection to: %s' % netloc)
            raise MockHttpCall(netloc)
        resp = self.old_send(request, *args, **kwargs)
        filename = os.path.join(file_save_path, netloc.replace(".", "_"))
        count = 0
        filename += str(count)
        while os.path.exists(filename):
            filename = filename[:-1] + str(count)
            count += 1
        with open(filename, "bw+") as download_content:
            download_content.write(resp.content)
        summaries.append(Mock(filename, netloc, path, request))
        return resp

    whitelisted.hooked = True

    if not getattr(requests.adapters.HTTPAdapter.send, 'hooked', False):
        logger.debug('Monkey patching ``requests.adapters.HTTPAdapter.send`` ')
        requests.adapters.HTTPAdapter.old_send = requests.adapters.HTTPAdapter.send
        requests.adapters.HTTPAdapter.send = whitelisted


def pytest_addoption(parser):
    group = parser.getgroup('blockhttp')
    group.addoption('--blockhttp', action='store_true',
                    help='Block network requests during test run')
    parser.addini(
        'blockhttp', 'Block network requests during test run', default=False)

    group.addoption(
        '--blockhttp-http-whitelist',
        action='store',
        help='Do not block HTTP requests to this comma separated list of '
             'hostnames',
        default=''
    )
    # TODO ???
    parser.addini(
        'blockhttp-http-whitelist',
        'Do not block HTTP requests to this comma separated list of hostnames',
        default=''
    )


def pytest_configure(config):
    if config.option.blockhttp or config.getini('blockhttp'):
        http_whitelist_str = config.option.blockhttp_http_whitelist or config.getini('blockhttp-http-whitelist')
        http_whitelist = http_whitelist_str.split(',')

        block_http(http_whitelist)


def pytest_unconfigure(config):
    print("Copy the following code to mock http call")
    for summary in summaries:
        print(template.format(summary))
