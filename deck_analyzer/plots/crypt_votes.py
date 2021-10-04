#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
from krcg import vtes
from ..deck import Deck


def get_votes(title: str) -> int:
    votes = {
        "Primogen": 1,
        "Prince": 2,
        "Justicar": 3,
        "Inner Circle": 4,
        "Baron": 2,
        "Bishop": 1,
        "Archbishop": 2,
        "Cardinal": 3,
        "Regent": 4,
        "Priscus": 3,
        "Magaji": 2,
        "1 vote": 1,
        "2 votes": 2,
    }
    return votes.get(title, 0)


def crypt_votes(deck: Deck, path):
    if not vtes.VTES:
        vtes.VTES.load()

    # X-axis
    x = ["0 Vote", "1 Vote", "2 Votes", "3 Votes", "4 Votes"]
    # Y-axis
    y = [0, 0, 0, 0, 0]

    for item in deck.get_crypt():
        for key in item.keys():
            y[get_votes(vtes.VTES[key].title)] += item[key]

    plt.bar(x, y, tick_label=x, width=0.8)

    plt.savefig(os.path.join(path, "crypt_votes.pdf"))
    plt.savefig(os.path.join(path, "crypt_votes.svg"))

    plt.clf()
    plt.cla()
