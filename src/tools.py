
import numpy as np
import pandas as pd

def clean(df,cols):
    xf = df
    cols = cols + ['G','MP']
    for c in cols:
        xf = xf.drop(xf.index[xf[c] == ''])

    return xf

def convert(df,cols):
    xf = df
    cols = cols + ['G','MP']
    for c in cols:
        xf[c] = xf[c].astype(float)

    return xf

def qualify(df,ngames=50,nmin=10):
    xf = df
    xf = xf.drop(xf.index[xf.G < ngames])
    xf = xf.drop(xf.index[xf.MP < nmin])

    return xf
