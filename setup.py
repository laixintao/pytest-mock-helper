# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='pytest-mock-helper',
    version='0.2.1',
    description='Help you mock HTTP call and generate mock code',
    long_description=(open('README.md').read() +
                      open('CHANGELOG.md').read()),
    license='BSD',
    install_requires=['pytest'],
    py_modules=['pytest_mock_helper'],
    entry_points={'pytest11': ['pytest_mock_helper = pytest_mock_helper']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
