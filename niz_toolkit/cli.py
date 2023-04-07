import argparse
import logging
import sys
from .calib import calib, lock_cli, unlock_cli


def main():
    parser = argparse.ArgumentParser(description="Niz keyboard toolkit.")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("--debug", action="store_true", help="debug")
    subcmd = parser.add_subparsers(metavar="subcmd")
    subcmd.required = True
    parser_calib = subcmd.add_parser("lock", help="Lock")
    parser_calib.set_defaults(func=lock_cli)
    parser_calib = subcmd.add_parser("unlock", help="Unlock")
    parser_calib.set_defaults(func=unlock_cli)
    parser_calib = subcmd.add_parser("calib", help="Calibration")
    parser_calib.set_defaults(func=calib)
    args = parser.parse_args()

    level = logging.WARN
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    )

    args.func(args)


if __name__ == "__main__":
    main()
