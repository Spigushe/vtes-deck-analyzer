#!/usr/bin/env python3
import os
import sys
import logging
import shutil


from .deck import Deck
from .plots.crypt_curve import crypt_curve
from .plots.crypt_disc import crypt_disc
from .plots.crypt_votes import crypt_votes
from .plots.library_types import library_types


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")

    fn = sys.argv[1]
    if os.path.exists(fn):
        logging.info("File exists: " + os.path.basename(fn))

        # Create a directory to temp save files
        dir_name = os.path.basename(fn)[: os.path.basename(fn).rfind(".")]
        dir_name = os.path.join(os.path.dirname(fn), dir_name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        deck = Deck()
        deck.from_file(fn)

        # Graphics generators
        crypt_curve(deck, dir_name)
        logging.info("Crypt curve generated")
        crypt_disc(deck, dir_name)
        logging.info("Discipline curve generated")
        crypt_votes(deck, dir_name)
        logging.info("Vote curve generated")
        library_types(deck, dir_name)
        logging.info("Types curve generated")

        # Delete the temp dir
        try:
            shutil.rmtree(dir_name)
            logging.info("Directory removed")
        except OSError as e:
            logging.error("Error: %s - %s." % (e.filename, e.strerror))

    else:
        logging.error("File does not exists: " + os.path.basename(fn))


if __name__ == "__main__":
    main()
