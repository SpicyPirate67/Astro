
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x_data = [0.0265, 0.0502, 0.0658, 0.0846, 0.0948, 0.1367]
y_data_spiral = [19, 32.18, 17.10, 18.22, 31.58, 39.47]
y_data_elliptical = [81, 67.814, 82.89, 81.77, 68.42, 60.52]

y_data = [i / y_data_elliptical[y_data_spiral.index(i)] for i in y_data_spiral]

ax.scatter(x_data, y_data)
ax.plot(np.unique(x_data), np.poly1d(np.polyfit(x_data, y_data, 1))(np.unique(x_data)), label="Best Fit")

plt.title("Galaxy Type aganst Redshift")
plt.xlabel("Redshift")
plt.ylabel("Spiral / Elliptical")
plt.legend(loc='upper left')
plt.show()
