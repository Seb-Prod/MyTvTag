import base64
from dataclasses import dataclass
from tvdb_v4_official import TVDB
import re
import time
from dotenv import load_dotenv
import os
@dataclass
class show:
    series: tuple
    saison: int
    episode: int


@dataclass
class episode:
    id: int
    num: int


@dataclass
class Saison:
    saison: tuple
    episode: tuple
    genre:str


@dataclass
class serie_info:
    id: str
    nom: str
    resume: str
    image: str


@dataclass
class info_episode:
    id: int
    saison: int
    num: int

@dataclass
class tag_episode:
    titre:str
    date:str
    resume:str

load_dotenv()

api_key = os.getenv('THETVDB_API_KEY')  # Obtenue sur TheTVDB
tvdb = TVDB(api_key)


def extract_info(filename):
    pattern = r"^(?P<serie>.+?)\.S(?P<season>\d{2})E(?P<episode>\d{2})"

    match = re.match(pattern, filename)
    if match:
        return match.groupdict()
    else:
        return None

def remove_point(name):
    return name.replace(".", " ")

def find_serie_name(file_name) -> show:
    info = extract_info(file_name)
    if info:
        name = remove_point(info['serie'])
        series = tvdb.search(name)

        # boucle qui récupère le noms des séries trouvé et les ID
        tableau_liste_series = []
        for serie in series:

            serie_id = serie['tvdb_id']
            cles = serie.keys()
            #print(cles)
            #print('##########')
            if serie['primary_type'] == "series":
                #print(serie)
                #print('#################')
                if "overviews" in serie:
                    if 'fra' in serie['overviews']:
                        serie_resume = serie['overviews']['fra']
                    elif 'overview' in serie:
                        serie_resume = serie['overview']
                elif 'overview' in serie:
                        serie_resume = serie['overview']
                else:
                    serie_resume = ""

                if 'translations' in serie:
                    if 'fra' in serie['translations']:
                        serie_nom = serie['translations']['fra']
                    else:
                        serie_nom = serie['name']
                else:
                    serie_nom = serie['name']

                if 'thumbnail' in serie:
                    image = serie['thumbnail']
                else:
                    image = serie['image_url']

                tableau_liste_series.append(serie_info(
                    id=serie_id, nom=serie_nom, resume=serie_resume, image=image))

        return show(series=tableau_liste_series, saison=info['season'], episode=info['episode'])
    else:
        return []

def find_episodes(serie_id: int) -> Saison:
    info = tvdb.get_series_episodes(serie_id, page=0)
    time.sleep(1)
    genres = tvdb.get_series_extended(serie_id)
    tableau_episode_liste = []

    tableau_saison = []
    tableau_retour = []

    for ep in info["episodes"]:
        tableau_episode_liste.append(info_episode(
            id=ep['id'], saison=ep['seasonNumber'], num=ep['number']))

    # récupération des saison
    for item in tableau_episode_liste:
        if item.saison not in tableau_saison:
            tableau_saison.append(item.saison)

    if tableau_saison:
        # récupération des épisode par saison
        for item_saison in tableau_saison:
            tableau_retour.append(get_episode_of_season(tableau_episode_liste, item_saison))
    else:
        tableau_saison.append("vide")
    
    
    
    return Saison(saison=tableau_saison, episode=tableau_retour, genre=get_genre(genres['genres']))

def get_episode_of_season(episodes: tuple, saison:int)-> tuple:
    tableau_retour = []
    for item in episodes:
        if (item.saison == saison):
            #print(f"saison: {saison} - épisode : {item.num} - id : {item.id}")
            tableau_retour.append(episode(id=item.id, num=item.num))
    return tableau_retour

def get_genre(genres: tuple)->str:
    retour = ""
    for genre in genres:
        retour = retour + genre['name'] + ", "
    return retour[:-2]



def fetch_episode(id)->tag_episode:
    episode = tvdb.get_episode(id)
    time.sleep(1)
    try:
        episode_fr = tvdb.get_episode_translation(id=id, lang="fra")
    except:
        episode_fr = []
        
    titre = ""
    resume = ""
    date = episode['aired']
    
    if len(episode_fr) > 0:
        if episode_fr['name']:
            titre = episode_fr['name']
        else:
            titre = episode['name']
            
        if episode_fr['overview']:
            resume = episode_fr['overview']
        else:
            resume = episode_fr['overview']
    else:
        titre = episode['name']
        resume = episode['overview']
    
    return tag_episode(titre=titre, date=date, resume=resume)
    