import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import serial

PROGRESSBAR_LIMIT = 100000
INCREMENT_FACTOR = 10
AMPLIFICATION_RATE = 1

# Configuration du thème sombre
customtkinter.set_appearance_mode("Dark")

# Fonction de mise à jour pour l'oscilloscope
class Scope:
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 3.3)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt >= self.tdata[0] + self.maxt:
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[0] + len(self.tdata) * self.dt

        self.tdata.append(t)
        self.ydata.append(y)

        self.line.set_data(self.tdata, self.ydata)
        self.ax.set_xlim(self.tdata[0], self.tdata[-1] + self.dt)

        return self.line,

# Fonction pour mettre à jour l'amplification
def update_amplification():
    global AMPLIFICATION_RATE
    AMPLIFICATION_RATE *= INCREMENT_FACTOR
    if AMPLIFICATION_RATE > PROGRESSBAR_LIMIT:
        AMPLIFICATION_RATE = 1
    progressbar.set(AMPLIFICATION_RATE / PROGRESSBAR_LIMIT)
    amplification_label.configure(text="Taux d'amplification : {}".format(AMPLIFICATION_RATE))

# Fonction pour le générateur de données
def emitter(p=0.1):
    ser = serial.Serial("COM4", baudrate=9600, timeout=1)
    ser.write(bytearray('S','ascii'))

    while True:
        bs = ser.readline()
        bs_decoded = bs.decode('utf-8').strip()
        if bs_decoded:
            try:
                y_value = float(bs_decoded)
            except ValueError:
                y_value = 0.0
        else:
            y_value = 0.0

        yield y_value

# Création de la fenêtre principale
app = customtkinter.CTk()
app.title('Oscilloscope GEii')

# Création du titre au milieu en haut
title_label = customtkinter.CTkLabel(app, text="Oscilloscope GEii", font=("Helvetica", 22, "bold"), text_color=("white", "gray75"))
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky="nsew")

# Création du bouton switch avec le texte 
switch_button = customtkinter.CTkSwitch(app, text="AC/DC", font=("Helvetica", 16, "bold"))
switch_button.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

# Création de la barre de progression avec le bouton
progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal", width=100, height=20)
progressbar.set(AMPLIFICATION_RATE / PROGRESSBAR_LIMIT)
progressbar.grid(row=1, column=1, pady=(10, 0), padx=(0, 30), sticky="e")

# Création du bouton pour augmenter l'amplification
button = customtkinter.CTkButton(app, text="Augmenter l'amplification", font=("Helvetica", 12, "bold"), command=update_amplification)
button.grid(row=2, column=1, pady=(10, 20), padx=(0, 10), sticky="e")

# Création du label pour afficher la valeur de la barre de progression
amplification_label = customtkinter.CTkLabel(app, text="Taux d'amplification : {}".format(AMPLIFICATION_RATE), font=("Helvetica", 14, "bold"))
amplification_label.grid(row=3, column=1, pady=(0, 20), padx=(0, 10), sticky="e")

# Création du cadre pour les signaux en direct
signals_canvas = customtkinter.CTkCanvas(app, background="gray10", highlightbackground="white", width=300, height=150)
signals_canvas.grid(row=4, column=0, columnspan=2, pady=(20, 20), sticky="nsew")

# Ajout d'un titre au cadre des signaux en direct
signals_label = customtkinter.CTkLabel(signals_canvas, text="Signaux en direct", font=("Helvetica", 16, "bold"))
signals_label.place(relx=0.5, rely=0.02, anchor="n")

# Ajout du graphique de l'oscilloscope dans le cadre des signaux en direct
fig, ax = plt.subplots()
scope = Scope(ax)
canvas = FigureCanvasTkAgg(fig, master=signals_canvas)
canvas.get_tk_widget().pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=1)
canvas.draw()

# Configurer l'animation de l'oscilloscope
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=50, blit=True, save_count=100)

# Configuration du poids des colonnes pour que le titre et le bouton soient centrés
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Configuration du poids des lignes pour le cadre des signaux en direct
app.grid_rowconfigure(4, weight=1)

# Lancer l'application
app.mainloop()