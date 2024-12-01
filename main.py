
import os
from tkinter import PhotoImage, StringVar
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk
import io
import base64
import video_tag
import online_tag as tag
import requests
import initialisation_affichage as my_app_init
import actualisation_affichage as my_app_maj

# Fenetre
app = ctk.CTk()

# ---------------------------- #
# Initialisations des varables #
# ---------------------------- #

# Tag video MP4
my_video_tag: video_tag.tag = video_tag.init_video_tag()
# Résultat de la requette tvdb qui liste le nom des série
ma_requette: tag.show = None

# Nom du fichier ouvert
file = "Halo.S02E03.FRENCH.WEBRip.x264-Wawacity.run.mp4"
# Nom du répertoire du fichier
folder = "/Volumes/Macintosh HD/Users/seb/Downloads"

# Liste des noms des séries trouvé
liste_des_noms_de_series = [""]
# Liste des saisons disponible
liste_des_numeros_des_saisons = [""]
# Liste des épisodes disponible
liste_des_numeros_des_episode = [""]
# Liste des Id tvdb des séries trouvé
liste_des_id_des_series = [""]
# Liste des résumé des séries trouvé
liste_des_resume_series = [""]
# Liste des résumé des épisode de la saison
liste_des_resume_episode = [""]
# Liste des liens vers les illustrations trouvé
liste_des_illustration_series = [""]
# Liste de tous les épisode de la série
liste_de_tout_les_episodes: tag.Saison = None
# Id liste série actif
active_id_serie = 0
# Liste des Id tvdb des épisodes trouvé
liste_des_id_des_episodes = [""]

numero_saison = 1
numero_episode = 1

index_list_saison = 0
index_list_episode = 0

# ------------------------------------- #
# Initialisation des éléménts graphique #
# ------------------------------------- #

# -- Frames -- #
frame_menu = ctk.CTkFrame(app)
frame_tag = ctk.CTkFrame(app)
frame_info = ctk.CTkFrame(frame_tag)

# -- Boutons -- #
bouton_ouvrir_fichier = ctk.CTkButton(frame_menu)
bouton_cherche_information = ctk.CTkButton(frame_menu)

# -- Zone de saisie -- #
saisie_nom_fichier = ctk.CTkEntry(frame_menu)

# -- Liste déroulante -- #
liste_deroulante_nom_serie = ctk.CTkOptionMenu(frame_tag)
liste_deroulante_season = ctk.CTkOptionMenu(frame_tag)
liste_deroulante_episode = ctk.CTkOptionMenu(frame_tag)

# -- TextBox -- #
textBox_titre_episode = ctk.CTkTextbox(frame_info)
textBox_date_episode = ctk.CTkTextbox(frame_info)
textBox_genre_episode = ctk.CTkTextbox(frame_info)
textBox_resume_serie = ctk.CTkTextbox(frame_info)
textBox_resume_episode = ctk.CTkTextbox(frame_info)

# __ Illustration -- #
illustration = ctk.CTkLabel(frame_info)

# -------- #
# CallBack #
# -------- #


def action_bouton_ouvre_fichier():
    global saisie_nom_fichier, my_video_tag, file, folder
    
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier",
        filetypes=[("Tous les fichiers", "*.mp4")]
    )
    if file_path:
        # Faire quelque chose avec le chemin du fichier sélectionné
        print(f"Fichier sélectionné : {file_path}")
    
    
    file = os.path.basename(file_path)
    folder = os.path.dirname(file_path)
    
    print(file)
    print(folder)
    
    # Efface la zone de saisie
    saisie_nom_fichier.delete(0, ctk.END)
    # Ecrit le nom du fichier dans la zone de saisie
    saisie_nom_fichier.insert(0, file)
    # Recupération des données stokées dans le MP4
    my_video_tag = video_tag.get_video_tag(f"{folder}/{file}")
    # Affiche les données
    affichage_des_metaDanees_du_mp4()


def action_bouton_charge_donnee_tvdb():
    global liste_des_episode, ma_requette, active_id_serie, numero_saison, numero_episode, index_list_episode

    # Lance la requette qui liste les nom des séries touvées
    ma_requette = tag.find_serie_name(file)
    numero_saison = int(ma_requette.saison)
    numero_episode = int(ma_requette.episode)
    # print(ma_requette)
    efface_les_listes()
    actualise_les_listes_serie_requette_tvdb()

    recuperation_liste_de_tout_les_episode()
    index_list_episode = recuperation_index_liste_deroulante(
        liste_deroulante_episode, liste_des_numeros_des_episode)

    tag_episode: tag.tag_episode = tag.fetch_episode(
        int(liste_des_id_des_episodes[index_list_episode]))
    actualisation_nouveau_tag(tag_episode)

    actualisation_tag_serie(0)


def action_liste_serie(_):
    global active_id_serie, index_list_episode
    selected_value = liste_deroulante_nom_serie.get()
    active_id_serie = liste_des_noms_de_series.index(selected_value)

    recuperation_liste_de_tout_les_episode()
    index_list_episode = recuperation_index_liste_deroulante(
        liste_deroulante_episode, liste_des_numeros_des_episode)

    tag_episode: tag.tag_episode = tag.fetch_episode(
        int(liste_des_id_des_episodes[index_list_episode]))
    actualisation_nouveau_tag(tag_episode)
    actualisation_tag_serie(active_id_serie)


def action_liste_saison(_):
    actulisation_liste_des_episode()
    index_list_episode = recuperation_index_liste_deroulante(
        liste_deroulante_episode, liste_des_numeros_des_episode)
    tag_episode: tag.tag_episode = tag.fetch_episode(
        int(liste_des_id_des_episodes[index_list_episode]))
    actualisation_nouveau_tag(tag_episode)
    actualisation_tag_serie(active_id_serie)
    
def action_liste_episode(_):
    index_list_episode = recuperation_index_liste_deroulante(
        liste_deroulante_episode, liste_des_numeros_des_episode)
    tag_episode: tag.tag_episode = tag.fetch_episode(
        int(liste_des_id_des_episodes[index_list_episode]))
    actualisation_nouveau_tag(tag_episode)
    actualisation_tag_serie(active_id_serie)
# --------- #
# Fonctions #
# --------- #


def affichage_des_metaDanees_du_mp4():
    # Efface les listes
    efface_les_listes()
    # Remplie les listes avec les donnée récupé dans le mp4
    liste_des_noms_de_series.append(my_video_tag.artist)
    liste_des_numeros_des_saisons.append(str(my_video_tag.tv_season))
    liste_des_numeros_des_episode.append(str(my_video_tag.tv_episode))
    # Actualisation des listes déroulante avec les donnée des listes
    actualisation_des_listes_deroulantes()
    # Actualisation des textes avec les données
    actualisation_des_textBox()
    # Affiche l'affiche de la série
    my_app_maj.actualisation_illustation_base_64(
        illustration, image=my_video_tag.image, max_width=200, max_height=200)


def actualise_les_listes_serie_requette_tvdb():
    for item in ma_requette.series:
        liste_des_id_des_series.append(int(item.id))
        liste_des_noms_de_series.append(item.nom)
        liste_des_resume_series.append(item.resume)
        liste_des_illustration_series.append(item.image)
    my_app_maj.actualisation_liste(
        liste_deroulante_nom_serie, liste_des_noms_de_series, liste_des_noms_de_series[0])


def efface_les_listes():
    liste_des_noms_de_series.clear()
    liste_des_numeros_des_saisons.clear()
    liste_des_numeros_des_episode.clear()
    liste_des_id_des_series.clear()
    liste_des_resume_series.clear()
    liste_des_illustration_series.clear()


def actualisation_des_listes_deroulantes():
    my_app_maj.actualisation_liste(
        liste_deroulante_nom_serie, liste_des_noms_de_series, 0)
    my_app_maj.actualisation_liste(
        liste_deroulante_season, liste_des_numeros_des_saisons, 0)
    my_app_maj.actualisation_liste(
        liste_deroulante_episode, liste_des_numeros_des_episode, 0)


def actualisation_des_textBox():
    my_app_maj.actualisation_textBox(textBox_titre_episode, my_video_tag.name)
    my_app_maj.actualisation_textBox(textBox_date_episode, my_video_tag.year)
    my_app_maj.actualisation_textBox(textBox_genre_episode, my_video_tag.genre)
    my_app_maj.actualisation_textBox(
        textBox_resume_serie, my_video_tag.tv_description)
    my_app_maj.actualisation_textBox(
        textBox_resume_episode, my_video_tag.long_description)


def actualisation_tag_serie(index: int):
    my_video_tag.tv_description = liste_des_resume_series[index]
    # my_video_tag.genre =
    my_app_maj.actualisation_illustration_lien_web(
        label=illustration, image=liste_des_illustration_series[index], max_width=200, max_height=200)
    actualisation_des_textBox()


def recuperation_liste_de_tout_les_episode():
    global liste_de_tout_les_episodes, active_id_serie

    liste_de_tout_les_episodes = tag.find_episodes(
        liste_des_id_des_series[active_id_serie])

    my_video_tag.genre = liste_de_tout_les_episodes.genre
    actualisation_liste_des_saison()
    actulisation_liste_des_episode()


def actualisation_liste_des_saison():
    global liste_des_numeros_des_saisons
    liste_des_numeros_des_saisons.clear()
    for saison in liste_de_tout_les_episodes.saison:
        liste_des_numeros_des_saisons.append(str(saison))
    my_app_maj.actualisation_liste(
        liste_deroulante_season, liste_des_numeros_des_saisons, numero_saison)


def actulisation_liste_des_episode():
    global liste_des_numeros_des_episode, index_list_saison, liste_des_id_des_episodes
    liste_des_numeros_des_episode.clear()
    liste_des_id_des_episodes.clear()
    index_list_saison = recuperation_index_liste_deroulante(
        liste_deroulante_season, liste_des_numeros_des_saisons)

    try:
        for episode in liste_de_tout_les_episodes.episode[index_list_saison]:
            liste_des_numeros_des_episode.append(str(episode.num))
            liste_des_id_des_episodes.append(episode.id)
    except:
        liste_des_numeros_des_episode.append("vide")

    my_app_maj.actualisation_liste(
        liste_deroulante_episode, liste_des_numeros_des_episode, numero_episode)


def recuperation_index_liste_deroulante(liste: ctk.CTkOptionMenu, options: tuple):
    selected_value = liste.get()
    # print(selected_value)

    index = options.index(selected_value)
    return index


def actualisation_nouveau_tag(tag: tag.tag_episode):
    my_video_tag.name = tag.titre
    my_video_tag.year = tag.date
    my_video_tag.long_description = tag.resume
# ---------- #
# a vérifier #
# ---------- #


def action_test(f):
    print(f"une action {f}")


def initialisation_app():
    my_app_init.initialisation_fenetre(app, 620, 590)

    my_app_init.initialisation_frame(frame=frame_menu, x=0, y=0)
    my_app_init.initialisation_frame(frame=frame_tag, x=0, y=90)
    my_app_init.initialisation_frame_info(frame=frame_info)

    my_app_init.initialisation_bouton(
        bouton=bouton_ouvrir_fichier, text="ouvir", column=0, command=action_bouton_ouvre_fichier)
    my_app_init.initialisation_bouton(
        bouton_cherche_information, text="tag", column=2, command=action_bouton_charge_donnee_tvdb)
    my_app_init.initialisation_zone_saisie(saisie_nom_fichier)

    my_app_init.initialisation_liste_deroulante(
        liste_deroulante_nom_serie, values=liste_des_noms_de_series, width=300, row=0, column=0, command=action_liste_serie)
    my_app_init.initialisation_liste_deroulante(
        liste_deroulante_season, values=liste_des_numeros_des_saisons, width=60, row=0, column=2, command=action_liste_saison)
    my_app_init.initialisation_liste_deroulante(
        liste_deroulante_episode, values=liste_des_numeros_des_episode, width=60, row=0, column=4, command=action_liste_episode)

    label_season = ctk.CTkLabel(frame_tag)
    label_episode = ctk.CTkLabel(frame_tag)
    my_app_init.initialisation_label(
        label=label_season, row=0, column=1, text="Saison n°")
    my_app_init.initialisation_label(
        label=label_episode, row=0, column=3, text="Episode n°")

    label_info_titre = ctk.CTkLabel(frame_info)
    label_info_date = ctk.CTkLabel(frame_info)
    label_info_genre = ctk.CTkLabel(frame_info)
    label_info_resume = ctk.CTkLabel(frame_info)
    label_info_resume_episode = ctk.CTkLabel(frame_info)
    label_info_affiche = ctk.CTkLabel(frame_info)
    my_app_init.initialisation_label(
        label_info_titre, row=0, column=0, text="Titre :", sticky="ne")
    my_app_init.initialisation_label(
        label_info_date, row=1, column=0, text="Date de sortie :", sticky="ne")
    my_app_init.initialisation_label(
        label_info_genre, row=2, column=0, text="Genre :", sticky="ne")
    my_app_init.initialisation_label(
        label_info_resume, row=3, column=0, text="Résumé de la série :", sticky="ne")
    my_app_init.initialisation_label(
        label_info_resume_episode, row=4, column=0, text="Résumé de l'épisode :", sticky="ne")
    my_app_init.initialisation_label(
        label_info_affiche, row=5, column=0, text="Affiche :", sticky="ne")

    my_app_init.initialisation_text_box(
        textBox_titre_episode, text="", height=20, width=400, row=0, column=1)
    my_app_init.initialisation_text_box(
        textBox_date_episode, text="", height=20, width=400, row=1, column=1)
    my_app_init.initialisation_text_box(
        textBox_genre_episode, text="", height=20, width=400, row=2, column=1)
    my_app_init.initialisation_text_box(
        textBox_resume_serie, text="", height=80, width=400, row=3, column=1)
    my_app_init.initialisation_text_box(
        textBox_resume_episode, text="", height=80, width=400, row=4, column=1)

    my_app_init.initialisation_label(illustration, row=5, column=1, text='')

    liste_deroulante_nom_serie.set(liste_des_noms_de_series[0])
    liste_deroulante_season.set(liste_des_numeros_des_saisons[0])
    liste_deroulante_episode.set(liste_des_numeros_des_episode[0])


def main():
    initialisation_app()
    app.mainloop()


if __name__ == "__main__":
    main()
