import base64
import io
import customtkinter as ctk
from PIL import Image
import requests

def actualisation_liste(liste:ctk.CTkOptionMenu, values: tuple, index:str):
    #print(f"index : {index}")
    if values:
        liste.configure(values=values)
        
    if str(index) in values:
        #print(f'{index} existe')
        liste.set(str(index))
    else:
        liste.set(values[0])
        ##print(f'{index} existe pas')
        #print(values)
    
    

def actualisation_textBox(textBox:ctk.CTkTextbox, text:str):
    textBox.delete('1.0', 'end')
    #print(f"texte : {text}")
    if text == None:
        text = ""
        
    textBox.insert("1.0", text)
    
def actualisation_illustation_base_64(label:ctk.CTkLabel,image:str, max_width:int, max_height:int):
    if not image == None:
        image_data = base64.b64decode(image)
        pil_image = Image.open(io.BytesIO(image_data))
    
        width, height = pil_image.size
    
        new_width = max_width
        new_height = max_height
    
    
        if height > width:
            new_height = max_height
            new_width = int(width * max_height / height)
        else:
            new_width=max_width
            new_height = int(height * max_width / width)
    
        tk_image =  ctk.CTkImage(light_image=pil_image, size=(new_width,new_height))
    
        label.configure(image=tk_image)
    
def actualisation_illustration_lien_web(label: ctk.CTkLabel, image:str, max_width:int, max_height:int):
    try:
        # Télécharger l'image
        response = requests.get(image, stream=True)
        response.raise_for_status()

        # Créer un objet Image à partir du contenu
        pil_image = Image.open(io.BytesIO(response.content))

        width, height = pil_image.size
    
        new_width = max_width
        new_height = max_height
    
        if height > width:
            new_height = max_height
            new_width = int(width * max_height / height)
        else:
            new_width=max_width
            new_height = int(height * max_width / width)
    
        tk_image =  ctk.CTkImage(light_image=pil_image, size=(new_width,new_height))
    
        label.configure(image=tk_image)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")


    