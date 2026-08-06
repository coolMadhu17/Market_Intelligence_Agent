import os


def ensure_directories():

    folders = [

        "output",

        "output/raw",

        "output/markdown",

        "output/excel",

        "output/logs"

    ]

    for folder in folders:

        os.makedirs(folder, exist_ok=True)