# Python URL Benchmark

[![Build Status](https://travis-ci.org/avara1986/python-url-benchmark.svg?branch=master)](https://travis-ci.org/avara1986/python-url-benchmark)
[![Coverage Status](https://coveralls.io/repos/github/avara1986/python-url-benchmark/badge.svg?branch=master)](https://coveralls.io/github/avara1986/python-url-benchmark?branch=master)
[![Requirements Status](https://requires.io/github/avara1986/python-url-benchmark/requirements.svg?branch=master)](https://requires.io/github/avara1986/python-url-benchmark/requirements/?branch=master)
[![Updates](https://pyup.io/repos/github/avara1986/python-url-benchmark/shield.svg)](https://pyup.io/repos/github/avara1986/python-url-benchmark/)
[![Python 3](https://pyup.io/repos/github/avara1986/python-url-benchmark/python-3-shield.svg)](https://pyup.io/repos/github/avara1986/python-url-benchmark/)


## Installation

From github:

```bash
git clone https://github.com/avara1986/python-url-benchmark.git
cd python-url-benchmark
pipenv install 
python url_benchmark.py http://0.0.0.0:8880/my-path 200 -H "accept: application/json" -H "Accept-Language: en"
```

# Help

```bash
$ python url_benchmark.py -h   

                                                                                                         
usage: url_benchmark.py [-h] [-H [HEADER [HEADER ...]]] [-v VERBOSE]
                        url retries

Python URL Benchmark

positional arguments:
  url                   Url to check
  retries               Number of requests to the URL

optional arguments:
  -h, --help            show this help message and exit
  -H [HEADER [HEADER ...]], --header [HEADER [HEADER ...]]
                        Headers to attach
  -v VERBOSE, --verbose VERBOSE
                        Verbose
```