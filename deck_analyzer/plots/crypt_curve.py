#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
from krcg import vtes
from ..deck import Deck


def crypt_curve_plot(deck: Deck, path: str):
    # X-axis
    x = range(1, 11 + 1)
    # Y-axis
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for item in deck.get_crypt():
        y[vtes.VTES[item["name"]].capacity - 1] = (
            y[vtes.VTES[item["name"]].capacity - 1] + item["count"]
        )

    plt.bar(x, y, tick_label=x, width=0.8, color="C0")

    plt.title("Crypt by capacity")
    plt.savefig(os.path.join(path, "crypt_curve.pdf"))
    plt.savefig(os.path.join(path, "crypt_curve.svg"))

    plt.clf()
    plt.cla()


def crypt_curve(deck: Deck, path: str):
    if not vtes.VTES:
        vtes.VTES.load()

    # Generating plots
    crypt_curve_plot(deck, path)
