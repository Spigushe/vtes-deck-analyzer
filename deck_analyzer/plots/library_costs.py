#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
import numpy as np
from krcg import vtes
from ..deck import Deck


def cost_sort(labels: list, costs: list) -> list:
    temp = []
    for l in labels:
        if str(l) in costs.keys():
            temp.append(costs[str(l)])
        else:
            temp.append(0)
    return temp


def library_costs(deck: Deck, path: str):
    if not vtes.VTES:
        vtes.VTES.load()

    pool, blood = {}, {}
    for item in deck.get_library():
        for key in item.keys():
            if vtes.VTES[key].blood_cost:
                if vtes.VTES[key].blood_cost not in blood.keys():
                    blood[vtes.VTES[key].blood_cost] = 0
                blood[vtes.VTES[key].blood_cost] += item[key]
            if vtes.VTES[key].pool_cost:
                if vtes.VTES[key].pool_cost not in pool.keys():
                    pool[vtes.VTES[key].pool_cost] = 0
                pool[vtes.VTES[key].pool_cost] += item[key]

    labels = ["X", 1, 2, 3, 4, 5, 6]
    blood = cost_sort(labels, blood)
    pool = cost_sort(labels, pool)

    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    width = 0.35
    pool = ax.bar(x - width/2, pool, width, label='Pool cost')
    blood = ax.bar(x + width/2, blood, width, label='Blood cost')
    ax.legend()

    fig.tight_layout()

    plt.savefig(os.path.join(path, "library_costs.pdf"))
    plt.savefig(os.path.join(path, "library_costs.svg"))

    plt.clf()
    plt.cla()
