import customtkinter as ctk

couleur_fond = "white"


def initialisation_fenetre(app: ctk.CTk, width: int, height: int):
    app.title("MyTvTag")

    # Récupération de la taille de l'écran
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Taille de la fenetre
    window_width = width
    window_height = height

    # Calcul de la position pour center l'affichage
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Le reditionnement de l'écran
    # app.resizable(False, False)

    # Pasitione la fenetre avec la position trouvé
    #app.wm_attributes('-topmost', True)
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    #app.wm_attributes('-topmost', False)

def initialisation_frame(frame: ctk.CTkFrame, x: int, y: int):
    frame.configure(fg_color=couleur_fond)
    frame.place(x=x, y=y)
    frame.pack(padx=5, pady=5)

def initialisation_frame_info(frame: ctk.CTkFrame):
    frame.configure(width=600, fg_color=couleur_fond)
    frame.grid(row=1, columnspan=5)

def initialisation_bouton(bouton: ctk.CTkButton, text: str, column: int, command, row:int=0):
    bouton.configure(text=text, command=command)
    bouton.grid(row=row, column=column, padx=5, pady=5)

def initialisation_zone_saisie(entry: ctk.CTkEntry):
    entry.configure(placeholder_text="Ouvir une video")
    entry.grid(row=0, column=1, padx=5, pady=5)
    entry.configure(width=300)

def initialisation_liste_deroulante(optionMenu: ctk.CTkOptionMenu, values: tuple, width: int, column:int, row:int, command):
    optionMenu.configure(values=values, width=width, command=command)
    optionMenu.grid(row=row, column=column, padx=5, pady=5)
    
def initialisation_label(label:ctk.CTkLabel, text:str, row:int, column:int, sticky=""):
    label.configure(text=text)
    label.grid(row=row, column=column, padx=5, pady=5, sticky=sticky)
    
def initialisation_text_box(textBox:ctk.CTkTextbox,text:str, height:int, width:int, row:int, column:int):
    textBox.configure(width=width, height=height, fg_color=couleur_fond)
    textBox.insert("1.0", text)
    textBox.grid(row=row, column=column)
    