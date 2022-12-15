

import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

file = "/home/spicypirate/Documents/Uni/Astro Assignment/code/Skyserver_SQL11_9_2022 11_07_21 AM.xlsx"

class galaxy():
    def __init__(self, u, g, r, spiral, elliptical):
        self.u = u
        self.g = g
        self.r = r
        self.spiral = spiral
        self.elliptical = elliptical

def maggie_convertion(data):

    if (type(data) != float):
        return

    flux = data*10**9
    mag = 22.5 - (2.5*np.log10(flux))
    return mag

df = pd.read_excel(file)
    
fig, ax = plt.subplots()

x_data_spiral = np.array([])
y_data_spiral = np.array([])
x_data_elliptical = np.array([])
y_data_elliptical = np.array([])

for i, row in df.iterrows():
    u = maggie_convertion(row[7])
    g = maggie_convertion(row[8])
    r = maggie_convertion(row[9])

    spiral = row[16]
    elliptical = row[17]   
    
    try:
        u_g = u-g
        g_r = g-r

        if spiral:
                x_data_spiral = np.append(x_data_spiral, u_g)
                y_data_spiral = np.append(y_data_spiral, g_r)
        else:
                x_data_elliptical = np.append(x_data_elliptical, u_g)
                y_data_elliptical = np.append(y_data_elliptical, g_r)

    except:
        x_data_spiral = x_data_spiral

ax.scatter(x_data_spiral, y_data_spiral, marker="*", label="spiral")
ax.scatter(x_data_elliptical, y_data_elliptical, marker="X", label="elliptical")

line_x = np.linspace(0.5,2,100)
line_y = [-i+2.22 for i in line_x]

ax.plot(line_x, line_y, label="U-R=2.22")

plt.title("Colour Colour plot")
plt.xlabel("G-R")
plt.ylabel("U-G")
plt.legend(loc='upper left')

print(x_data_elliptical, y_data_elliptical)
print(x_data_spiral, y_data_spiral)

plt.show()

