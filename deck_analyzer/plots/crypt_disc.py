#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/index.html
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# https://stackoverflow.com/questions/44246650/add-image-annotations-to-bar-plots/44264051#44264051
import shutil
import requests
from krcg import vtes
from ..deck import Deck


def check_level(discipline: str) -> str:
    if discipline == discipline.lower():
        return "inf"
    return "sup"


def sort_disc(table: dict) -> dict:
    temp = []
    for key in table.keys():
        temp.append(
            (
                key,
                table[key]["sup"] + table[key]["inf"],
                table[key]["sup"],
                table[key]["inf"],
            )
        )
    # Default sorting: alphabetically
    temp = sorted(temp, key=lambda t: t[0])
    # Secondary sorting: quantity of sup DESC
    temp = sorted(temp, key=lambda t: t[2], reverse=True)
    # Primary sorting: quantity of tot DESC
    temp = sorted(temp, key=lambda t: t[1], reverse=True)
    return temp


def get_disc(d: str, dir_name: str):
    # File address
    path = os.path.join(dir_name, d.lower() + ".png")
    # Download discipline
    url = "https://static.krcg.org/png/disc/inf/{}.png".format(d.lower())
    response = requests.get(url, stream=True)
    with open(path, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    # Return picture
    im = plt.imread(path)
    return im


def offset_image(coord, name, ax, dir_name):
    img = get_disc(name, dir_name)
    im = OffsetImage(img, zoom=0.018)
    im.image.axes = ax

    ab = AnnotationBbox(
        im,
        (coord, 0),
        xybox=(0.0, -16.0),
        frameon=False,
        xycoords="data",
        boxcoords="offset points",
        pad=0,
    )

    ax.add_artist(ab)


def crypt_disc(deck: Deck, path):
    if not vtes.VTES:
        vtes.VTES.load()

    disc = {}
    for item in deck.get_crypt():
        for d in vtes.VTES[item["name"]].disciplines:
            if d.lower() not in disc.keys():
                disc[d.lower()] = {
                    "inf": 0,
                    "sup": 0,
                }
            disc[d.lower()][check_level(d)] += item["count"]
    keys = sort_disc(disc)

    inf, sup = [], []
    labels = []
    for k in keys:
        inf.append(disc[k[0]]["inf"] + disc[k[0]]["sup"])
        sup.append(disc[k[0]]["sup"])
        labels.append(k[0].upper())

    fig, ax = plt.subplots()
    inf = ax.bar(range(len(labels)), inf, width=0.8, label="Inferior", color="C1")
    sup = ax.bar(range(len(labels)), sup, width=0.8, label="Superior", color="C0")
    ax.axhline(0, color="grey", linewidth=0.8)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", which="major", pad=26)
    ax.legend()

    for i, c in enumerate(labels):
        offset_image(i, c, ax, path)

    plt.savefig(os.path.join(path, "crypt_disc.pdf"))
    plt.savefig(os.path.join(path, "crypt_disc.svg"))

    plt.clf()
    plt.cla()
