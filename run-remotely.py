#!/usr/bin/env python3
import argparse
import contextlib
import logging
import os
import shlex

from phablet import Phablet, SynchronizedDirectory


def main():
    logging.basicConfig(level=logging.DEBUG,
                        style='{', format="[{levelname:10}] {message}")
    parser = argparse.ArgumentParser()
    # parser.add_argument("cmd", nargs='+')
    parser.parse_args()
    phablet = Phablet()
    with contextlib.ExitStack() as stack:
        if os.path.exists("bin/"):
            bin_dir = stack.enter_context(
                SynchronizedDirectory("bin/", phablet))
        else:
            bin_dir = None
        if os.path.exists("units/"):
            units_dir = stack.enter_context(
                SynchronizedDirectory("units/", phablet))
        else:
            units_dir = None
        if os.path.exists('data/'):
            data_dir = stack.enter_context(
                SynchronizedDirectory("data/", phablet))
        else:
            data_dir = None
        test_cmd = []
        custom_env = {}
        if bin_dir is not None:
            custom_env['PLAINBOX_PROVIDER_BIN'] = bin_dir
        if units_dir is not None:
            custom_env['PLAINBOX_PROVIDER_UNITS'] = units_dir
        if data_dir is not None:
            custom_env['PLAINBOX_PROVIDER_DATA'] = data_dir
        # test_cmd.extend(ns.cmd)
        job_cmd = 'cat $PLAINBOX_PROVIDER_UNITS/jobs.txt'
        env_txt = ' '.join('{}={}'.format(key, value)
                           for key, value in sorted(custom_env.items()))
        test_cmd.extend([env_txt, '/bin/sh', '-c', shlex.quote(job_cmd)])
        print("The command we want to run: {0!r}".format(test_cmd))
        phablet.run(test_cmd)
        input("---")


if __name__ == '__main__':
    main()
