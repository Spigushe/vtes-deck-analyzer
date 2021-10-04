#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
from krcg import vtes
from ..deck import Deck


def library_types(deck: Deck, path: str):
    if not vtes.VTES:
        vtes.VTES.load()

    types = {}
    for item in deck.get_library():
        for key in item.keys():
            for t in vtes.VTES[key].types:
                if t not in types.keys():
                    types[t] = 0
                types[t] += item[key]

    fig, ax = plt.subplots()
    labels = [str(k) + " (" + str(v) + ")" for k, v in types.items()]
    values = [v for k, v in types.items()]
    ax.pie(values, labels=labels, startangle=90)

    plt.savefig(os.path.join(path, "library_types.pdf"))
    plt.savefig(os.path.join(path, "library_types.svg"))

    plt.clf()
    plt.cla()
