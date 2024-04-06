from rungekutta import main
import matplotlib.pyplot as plt

X, Y, U = main()
fig, ax = plt.subplots(2, 1)
ax[0].scatter(X, Y)
ax[1].scatter(X, U)
plt.show()



