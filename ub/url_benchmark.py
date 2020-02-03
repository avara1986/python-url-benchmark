import argparse
import asyncio
import sys
import time

from aiohttp import ClientSession


class Command:
    total_time = 0
    total_requests = 0
    total_errors = 0

    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        autorun = kwargs.get("autorun", True)
        if not arguments:
            arguments = sys.argv[1:]

        parser = argparse.ArgumentParser(description='Python URL Benchmark')
        parser.add_argument("url", type=str, help="Url to check")
        parser.add_argument("retries", type=int, help="Number of requests to the URL")
        parser.add_argument("-H", "--header", nargs='*', type=str, help="Headers to attach")
        parser.add_argument("-v", "--verbose", default="", type=str, help="Verbose ")
        self.headers = {}
        args = parser.parse_args(arguments)
        if args.header:
            for header in args.header:
                k, v = header.split(":")
                self.headers[k.strip()] = v.strip()
        self.url = args.url
        self.retries = args.retries
        self.verbose = len(args.verbose)
        print("Ready to check the URL: {} {} times".format(self.url, self.retries))
        if autorun:
            result = self.run()
            if result:
                self.exit_ok("OK")
            else:
                self.print_error("ERROR")

    def run(self):
        start = time.time()
        urls = [self.url, ] * self.retries
        futures = [self.call_url(urls[i], self.headers, i) for i in range(len(urls))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        loop.close()
        self.print_ok("TOTAL Requests: %s" % (self.total_requests))
        if self.total_errors > 0:
            self.print_error("TOTAL Requests with errors: %s" % (self.total_errors))
        else:
            self.print_ok("TOTAL Requests with errors: %s" % (self.total_errors))
        self.print_ok("TOTAL Requests time: %s" % (self.total_time))
        total_requests = self.total_requests + self.total_errors
        if total_requests > 0:
            self.print_ok("TOTAL time (averrage): %s" % (self.total_time / (self.total_requests + self.total_errors)))
        else:
            self.print_error("TOTAL time (averrage): ERROR")
        self.print_ok("TOTAL Elapsed Time: %s" % (time.time() - start))
        return True

    async def call_url(self, url, headers, position):
        start = time.time()
        self.print_verbose('[{}] Starting {}'.format(position, url))
        json_data = ""
        try:
            async with ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    json_data = await response.text()
                    total = time.time() - start
                    self.total_time += total

                    if response.status in [200, 201, 202, 203, 204, 205]:
                        self.print_verbose('[{}] End {}'.format(position, total))
                        self.total_requests += 1
                    else:
                        self.total_errors += 1
                        self.print_verbose('[{}] End {} with errors'.format(position, total))
                        json_data = False
        except Exception as e:
            print(e)
        return json_data

    @staticmethod
    def print_ok(msg=""):
        print('\033[92m\033[1m ' + msg + ' \033[0m\033[0m')

    def print_verbose(self, msg=""):
        if self.verbose:
            print(msg)

    @staticmethod
    def print_error(msg=""):
        print('\033[91m\033[1m ' + msg + ' \033[0m\033[0m')

    def exit_with_error(self, msg=""):
        self.print_error(msg)
        sys.exit(2)

    def exit_ok(self, msg=""):
        self.print_ok(msg)
        sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    cmd = Command(arguments=sys.argv[1:], autorun=False)
    cmd.run()
