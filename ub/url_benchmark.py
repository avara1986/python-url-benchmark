import argparse
import asyncio
import sys
import time

import aiohttp
import async_timeout


class Command:
    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        autorun = kwargs.get("autorun", True)
        if not arguments:
            arguments = sys.argv[1:]

        parser = argparse.ArgumentParser(description='Python URL Benchmark')
        parser.add_argument("url", type=str, help="Url to check")
        parser.add_argument("retries", type=int, help="Number of requests to the URL")

        args = parser.parse_args(arguments)
        self.url = args.url
        self.retries = args.retries
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
        futures = [self.call_url(urls[i], i) for i in range(len(urls))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        print("TOTAL Elapsed Time: %s" % (time.time() - start))
        return True

    async def fetch(self, session, url):
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()

    async def call_url(self, url, position):
        start = time.time()
        print('[{}] Starting {}'.format(position, url))
        async with aiohttp.ClientSession() as session:
            json_data = await self.fetch(session, url)
            if json_data:
                print('[{}] End {}'.format(position, time.time() - start))
            else:
                self.print_error('[{}] End {} with errors'.format(position, time.time() - start))

    @staticmethod
    def print_ok(msg=""):
        print('\033[92m\033[1m ' + msg + ' \033[0m\033[0m')

    @staticmethod
    def print_error(msg=""):
        print('\033[91m\033[1m ' + msg + ' \033[0m\033[0m')

    def exit_with_error(self, msg=""):
        self.print_error(msg)
        sys.exit(2)

    def exit_ok(self, msg=""):
        self.print_ok(msg)
        sys.exit(0)


if __name__ == '__main__':
    cmd = Command(arguments=sys.argv[1:], autorun=False)
    cmd.run()
