import requests
import os
from PIL import Image, ImageDraw, ImageFont
from .google_model import GoogleModel
from .local_model import LocalModel

google_model = GoogleModel()
local_model = LocalModel()

def fetch_lyrics(song_info: str) -> str:
    parts = song_info.split(" - ", 1)
    if len(parts) < 2:
        return "Formato incorrecto. Use 'Artista - Título'."
    artist, title = parts[0].strip(), parts[1].strip()
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            lyrics_text = data.get("lyrics", "").strip()
            return lyrics_text if lyrics_text else "No se encontró la letra para esa canción."
        else:
            return "No se encontró la letra para esa canción."
    except Exception as e:
        return f"Error al obtener la letra: {e}"

def generate_creative_prompt(lyrics_text: str) -> str:
    prompt_input = (
        "Dada la siguiente letra compleja y rica en detalles, genera un prompt artístico y descriptivo, de al menos 200 palabras, "
        "para crear una imagen digital de altísima calidad. Incluye detalles visuales, atmósfera cinematográfica, colores vibrantes, "
        "composición equilibrada y un estilo único. Interpreta la letra sin repetirla textualmente. Letra: " + lyrics_text
    )
    creative_prompt = google_model.get_response(prompt_input)
    if not creative_prompt or creative_prompt == "No se pudo obtener respuesta del modelo.":
        creative_prompt = local_model.get_response(prompt_input)
    return creative_prompt