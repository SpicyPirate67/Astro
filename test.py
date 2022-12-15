
import numpy as np

def maggie_convertion(data):

    if (type(data) != float):
        return

    flux = data*10**9
    mag = 22.5 - (2.5*np.log10(flux))
    return mag
