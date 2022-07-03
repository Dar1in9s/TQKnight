import os


def loadQSS(name):
    qssDir = os.path.dirname(__file__)
    filename = qssDir + "/" + name
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
