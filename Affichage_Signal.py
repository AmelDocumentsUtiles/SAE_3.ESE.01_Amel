import serial
import serial.tools.list_ports

import matplotlib.pyplot as plt

import matplotlib.animation as animation
from matplotlib.lines import Line2D

class Scope:
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 4)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt >= self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        # This slightly more complex calculation avoids floating-point issues
        # from just repeatedly adding `self.dt` to the previous value.
        t = self.tdata[0] + len(self.tdata) * self.dt

        self.tdata.append(t)
        self.ydata.append(y)

        # Tracer la nouvelle ligne
        self.line.set_data(self.tdata, self.ydata)

        # Mettre à jour les limites de l'axe pour suivre la progression du temps
        self.ax.set_xlim(self.tdata[0], self.tdata[-1] + self.dt)

        return self.line,

def emitter(p=0.1):
    """Return a random value in [0, 1) with probability p, else 0."""
    ser = serial.Serial("COM3", baudrate=115200, timeout=1)  #IL FAUT ADAPTER LE PORT EN FONCTION DU PC

    ser.write(bytearray('S','ascii'))

    while True:
        bs = ser.readline()
        bs_decoded = bs.decode('utf-8').strip()
        if bs_decoded:
            try:
                # Convertir la valeur reçue en un nombre
                y_value = float(bs_decoded)
            except ValueError:
                y_value = 0.0  # Si la conversion échoue, mettre la valeur par défaut à 0.0
        else:
            y_value = 0.0  # Si la chaîne est vide, mettre la valeur par défaut à 0.0

        yield y_value

# Créer la figure et l'axe
fig, ax = plt.subplots()
scope = Scope(ax)

# Passer un générateur à "emitter" pour produire des données pour la fonction de mise à jour (pour que ça fasse en direct)
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=50,
                              blit=True, save_count=100)

plt.show()