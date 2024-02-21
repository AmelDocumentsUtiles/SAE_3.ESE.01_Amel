import customtkinter

PROGRESSBAR_LIMIT = 100000
INCREMENT_FACTOR = 10

AMPLIFICATION_RATE = 1

def update_amplification():
    global AMPLIFICATION_RATE
    AMPLIFICATION_RATE *= INCREMENT_FACTOR
    if AMPLIFICATION_RATE > PROGRESSBAR_LIMIT:
        AMPLIFICATION_RATE = 1
    progressbar.set(AMPLIFICATION_RATE / PROGRESSBAR_LIMIT)
    amplification_label.configure(text="Taux d'amplification : {}".format(AMPLIFICATION_RATE))

# Configuration du thème sombre
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title('Oscilloscope GEii')

# Création du titre au milieu en haut
title_label = customtkinter.CTkLabel(app, text="Oscilloscope GEii", font=("Helvetica", 22, "bold"),
                                      text_color=("white", "gray75"))
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky="nsew")

# Création du bouton switch "AC/DC"
switch_button = customtkinter.CTkSwitch(app, text="AC/DC", font=("Helvetica", 16, "bold"))
switch_button.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

# Création de la barre de progression avec le bouton
progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal", width=100, height=20)
progressbar.set(AMPLIFICATION_RATE / PROGRESSBAR_LIMIT)
progressbar.grid(row=2, column=1, pady=(10, 0), padx=(0, 30), sticky="e")

# Création du bouton pour augmenter l'amplification
button = customtkinter.CTkButton(app, text="Augmenter l'amplification", font=("Helvetica", 12, "bold"), command=update_amplification)
button.grid(row=3, column=1, pady=(10, 20), padx=(0, 10), sticky="e")

# Création du label pour afficher la valeur de la barre de progression
amplification_label = customtkinter.CTkLabel(app, text="Taux d'amplification : {}".format(AMPLIFICATION_RATE), font=("Helvetica", 14, "bold"))
amplification_label.grid(row=1, column=1, pady=(0, 20), padx=(0, 10), sticky="e")

# Création du cadre pour les signaux en direct
signals_canvas = customtkinter.CTkCanvas(app, background="gray10", highlightbackground="white", width=300, height=150)
signals_canvas.grid(row=4, column=0, columnspan=2, pady=(20, 20), sticky="nsew")

# Ajout d'un titre au cadre des signaux en direct
signals_label = customtkinter.CTkLabel(signals_canvas, text="Signaux en direct", font=("Helvetica", 16, "bold"))
signals_label.place(relx=0.5, rely=0.02, anchor="n")

# Ajout du texte "Signal 1"
signal1_text = customtkinter.CTkLabel(signals_canvas, text=" - Signal 1", font=("Helvetica", 14, "bold"), text_color=("gold", "gold"))
signal1_text.place(relx=0.97, rely=0.05, anchor="n")

# Ajout du texte "Signal 2"
signal2_text = customtkinter.CTkLabel(signals_canvas, text=" - Signal 2", font=("Helvetica", 14, "bold"), text_color=("medium purple", "medium purple"))
signal2_text.place(relx=0.97, rely=0.12, anchor="n")

# Ajout des textes à droite pour simuler une liste à puces
bullet_texts = ["RUN", "Measures", "Cursor", "Menu", "CH1", "CH2"]
for index, bullet_text in enumerate(bullet_texts, start=1):
    bullet_label = customtkinter.CTkLabel(signals_canvas, text="⦿  " + bullet_text, font=("Helvetica", 12, "bold"), text_color="white")
    bullet_label.place(relx=0.97, rely=0.25 + 0.08 * index, anchor="n")

# Configuration du poids des colonnes pour que le titre et le bouton soient centrés
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Configuration du poids des lignes pour le cadre des signaux en direct
app.grid_rowconfigure(4, weight=1)

app.mainloop()