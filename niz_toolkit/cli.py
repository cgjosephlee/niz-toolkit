import argparse
import logging
import sys
from .calib import calib

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
)


def main():
    parser = argparse.ArgumentParser(description="Niz keyboard toolkit.")
    subcmd = parser.add_subparsers(metavar="subcmd")
    subcmd.required = True
    parser_calib = subcmd.add_parser("calib", help="Calibration")
    parser_calib.add_argument("--debug", action="store_true", help="Debug")
    parser_calib.set_defaults(func=calib)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
