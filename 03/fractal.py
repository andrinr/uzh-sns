import numpy as np
import matplotlib.pyplot as plt


def logistic(X_n, alpha):
    return alpha * X_n * (1 - X_n)


alphas = np.linspace(1, 4, 1000)
x = []
y = []
cutoff = 1000

for i in range(len(alphas)):

    X = 0.5
    sum = X

    for j in range(2000):
        X = logistic(X, alphas[i])

        if j > cutoff:
            x.append(alphas[i])
            y.append(X)


fig, ax = plt.subplots()

plt.scatter(x, y, 0.1, "black")

plt.show()