#!/usr/bin/env python3
import contextlib
import logging
import os
import subprocess
import argparse

from phablet import Phablet, SynchronizedDirectory


def main():
    logging.basicConfig(level=logging.INFO, style='{', format="[{levelname:10}] {message}")
    parser = argparse.ArgumentParser()
    parser.add_argument("script")
    parser.add_argument("args", nargs='...')
    ns = parser.parse_args()
    phablet = Phablet()
    with contextlib.ExitStack() as stack:
        bin_dir = stack.enter_context(SynchronizedDirectory("bin/", phablet))
        if os.path.exists("units/"):
            units_dir = stack.enter_context(SynchronizedDirectory("units/", phablet))
        else:
            units_dir = None
        if os.path.exists('data/'):
            data_dir = stack.enter_context(SynchronizedDirectory("data/", phablet))
        else:
            data_dir = None
        phablet.run([os.path.join(bin_dir, ns.script)] + ns.args)


if __name__ == '__main__':
    main()
