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


def sort_disc(table: dict) -> dict:
    temp = []
    for key in table.keys():
        temp.append((key, table[key]["tot"], table[key]["sup"], table[key]["inf"]))
    # Default sorting: alphabetically
    temp = sorted(temp, key=lambda t: t[0])
    # Secondary sorting: quantity of superior DESC
    temp = sorted(temp, key=lambda t: t[2], reverse=True)
    # Primary sorting: quantity of total DESC
    temp = sorted(temp, key=lambda t: t[1], reverse=True)
    return temp


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
                        "tot": 0,
                    }
                disc[d.lower()][check_level(d)] += item[key]
                disc[d.lower()]["tot"] += item[key]
    keys = sort_disc(disc)

    inf, sup = [], []
    labels = []
    for k in keys:
        inf.append(disc[k[0]]["inf"] * -1)
        sup.append(disc[k[0]]["sup"])
        labels.append(k[0].upper())

    fig, ax = plt.subplots()
    N = len(keys)
    ind = np.arange(N)
    sup = ax.bar(ind, sup, width=0.8, label="Superior")
    inf = ax.bar(ind, inf, width=0.8, label="Inferior")
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.savefig(os.path.join(path, "crypt_disc.pdf"))
    plt.savefig(os.path.join(path, "crypt_disc.svg"))

    plt.clf()
    plt.cla()
