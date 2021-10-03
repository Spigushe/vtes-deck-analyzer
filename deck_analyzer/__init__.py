#!/usr/bin/env python3
import os
import sys
import logging


from .deck import Deck


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")

    fn = sys.argv[1]
    if os.path.exists(fn):
        logging.info("File exists: " + os.path.basename(fn))

        deck = Deck()
        deck.from_file(fn)

    else:
        logging.error("File does not exists: " + os.path.basename(fn))


if __name__ == "__main__":
    main()
