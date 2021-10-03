#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
import numpy as np
from krcg import vtes
from ..deck import Deck


def check_level(discipline: str) -> str:
    if discipline == discipline.lower():
        return "inf"
    return "sup"


def crypt_disc(deck: Deck, path):
    if not vtes.VTES:
        vtes.VTES.load()

    disc = {}
    for item in deck.get_crypt():
        for key in item.keys():
            for d in vtes.VTES[key].disciplines:
                if d.lower() not in disc.keys():
                    disc[d.lower()] = {
                        "inf": 0,
                        "sup": 0,
                    }
                disc[d.lower()][check_level(d)] += item[key]

    keys = [k for k, v in disc.items()]
    keys.sort()

    inf, sup = [], []
    for k in keys:
        inf.append(disc[k]["inf"] * -1)
        sup.append(disc[k]["sup"])

    fig, ax = plt.subplots()
    N = len(keys)
    ind = np.arange(N)
    sup = ax.bar(ind, sup, width=0.8, label="Superior")
    inf = ax.bar(ind, inf, width=0.8, label="Inferior")
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_xticks(ind)
    ax.set_xticklabels(keys)
    ax.legend()

    plt.savefig(os.path.join(path, "crypt_disc.pdf"))
    plt.savefig(os.path.join(path, "crypt_disc.svg"))
