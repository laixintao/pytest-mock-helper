# Installation

```
pip install pytest-mock-helper
```

# Usage

In develop you need those enviroments:

```
export PYTEST_NETWORK_MOCK=develop
export PYTEST_NETWORK_FILEPATH=/tmp
```

For example you have a test file called test_request.py:

```
# -*- coding: utf-8 -*-

import requests


def test_requests_send(capsys):
    requests.get("https://httpbin.org")
```

Run with `--blockhtp`

```
$ pytest tests/test_requests.py --blockhttp
======================================================== test session starts =========================================================
platform darwin -- Python 3.6.4, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /Users/laixintao/Program/pytest-network-mock-helper, inifile:
plugins: mock-helper-0.0.2
collected 1 item

tests/test_requests.py .                                                                                                       [100%]

====================================================== 1 passed in 1.38 seconds ======================================================
Copy the following code to mock http call

@httmock.urlmatch(netloc="httpbin.org", path="/")
def mock_item(url, request):
    return test_utils.fake_response(
        rel_path="/tmp/httpbin_org0",
        url="https://httpbin.org/",
        status_code=200
    )
```

Also a downloaded file will be saved to your $PYTEST_NETOWRK_FILEPATH:

```
$ ls /tmp/httpbin_org0
ls /tmp/httpbin_org0
```

## In Production

The test server can't send any HTTP request by default:

```
pytest tests/test_requests.py --blockhttp
======================================================== test session starts =========================================================
platform darwin -- Python 3.6.4, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /Users/laixintao/Program/pytest-network-mock-helper, inifile:
plugins: mock-helper-0.0.2
collected 1 item

tests/test_requests.py F                                                                                                       [100%]

============================================================== FAILURES ==============================================================
_________________________________________________________ test_requests_send _________________________________________________________

capsys = <_pytest.capture.CaptureFixture object at 0x10a3c3898>

    def test_requests_send(capsys):
>       requests.get("https://httpbin.org")

tests/test_requests.py:7:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
../../.virtualenvs/pytest-plugin/lib/python3.6/site-packages/requests/api.py:72: in get
    return request('get', url, params=params, **kwargs)
../../.virtualenvs/pytest-plugin/lib/python3.6/site-packages/requests/api.py:58: in request
    return session.request(method=method, url=url, **kwargs)
../../.virtualenvs/pytest-plugin/lib/python3.6/site-packages/requests/sessions.py:508: in request
    resp = self.send(prep, **send_kwargs)
../../.virtualenvs/pytest-plugin/lib/python3.6/site-packages/requests/sessions.py:618: in send
    r = adapter.send(request, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <requests.adapters.HTTPAdapter object at 0x10a3c3e80>, request = <PreparedRequest [GET]>, args = ()
kwargs = {'cert': None, 'proxies': OrderedDict(), 'stream': False, 'timeout': None, ...}
parsed = ParseResult(scheme='https', netloc='httpbin.org', path='/', params='', query='', fragment=''), netloc = 'httpbin.org'
path = '/'

    def whitelisted(self, request, *args, **kwargs):
        global summaries
        parsed = urlparse(request.url)
        netloc = parsed.netloc
        path = parsed.path
        if isinstance(netloc, str) and netloc in whitelist:
            return self.old_send(request, *args, **kwargs)

        if not is_develop:
            logger.warning('Denied HTTP connection to: %s' % netloc)
>           raise MockHttpCall(netloc)
E           pytest_mock_helper.MockHttpCall: httpbin.org

pytest_mock_helper.py:53: MockHttpCall
-------------------------------------------------------- Captured stderr call --------------------------------------------------------
pytest_mock_helper.py       
```

