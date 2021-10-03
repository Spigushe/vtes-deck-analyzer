#!/usr/bin/env python3
from typing import Tuple
from krcg import vtes


class Deck:
    """Class"""

    # Deck data
    deck, crypt, library = [], [], []

    def __init__(self):
        if not vtes.VTES:
            vtes.VTES.load()

    def get_library(self):
        return self.library

    def get_crypt(self):
        return self.crypt

    @classmethod
    def from_file(self, input: str):
        with open(input, "r") as file:
            decklist = file.readlines()
        for line in decklist:
            if line != "\n":
                if line.strip()[:1] in "0123456789":
                    self.deck.append(line.strip())
        self.parse(self)

    def parse(self):
        for line in self.deck:
            count, name = self.get_card(line)
            if "Vampire" in vtes.VTES[name].types:
                self.crypt.append({name: count})
            else:
                self.library.append({name: count})

    def get_card(line: str) -> Tuple[int, str]:
        name, count = "", ""
        prev = ""
        for car in line:
            if car in "0123456789":
                count = count + car
            else:
                break
        for car in line[len(count) + 1 :].strip():
            if car == " " and prev == " ":
                name = name[:-1]
                break
            name = name + car
            prev = car
        return int(count), name
