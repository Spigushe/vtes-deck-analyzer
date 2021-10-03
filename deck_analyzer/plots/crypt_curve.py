#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
from krcg import vtes
from ..deck import Deck


def crypt_curve(deck: Deck, path):
    if not vtes.VTES:
        vtes.VTES.load()

    # X-axis
    x = range(1, 11 + 1)
    # Y-axis
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for item in deck.get_crypt():
        for key in item.keys():
            y[vtes.VTES[key].capacity - 1] = y[vtes.VTES[key].capacity - 1] + item[key]

    plt.bar(x, y, tick_label=x, width=0.8, color=["red", "green"])

    plt.savefig(os.path.join(path, "crypt_curve.pdf"))
    plt.savefig(os.path.join(path, "crypt_curve.svg"))
