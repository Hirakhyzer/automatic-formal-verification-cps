import numpy as np


def down(x):
    a = np.asarray(x, dtype=float)
    return np.nextafter(a, -np.inf)


def up(x):
    a = np.asarray(x, dtype=float)
    return np.nextafter(a, np.inf)
