import requests
import config
import os
from PIL import Image, ImageDraw, ImageFont

def fetch_lyrics(song_info: str) -> str:
    # Se espera que song_info tenga el formato "Artista - Título"
    parts = song_info.split(" - ", 1)
    if len(parts) < 2:
        return "Formato incorrecto. Use 'Artista - Título'."
    artist, title = parts[0].strip(), parts[1].strip()
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get("lyrics", "No se encontraron letras.")
            return lyrics
        else:
            return "No se encontraron letras."
    except Exception as e:
        return f"Error al obtener la letra: {e}"

def main():
    with open("lyrics.txt", "r", encoding="utf-8") as f:
        lyrics = f.read()
    
    img = Image.new(
        "RGB",
        (config.IMAGE_WIDTH, config.IMAGE_HEIGHT),
        color=config.BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(img)
    
    font_path = config.FONT_PATH
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        try:
            font = ImageFont.truetype(font_path, config.FONT_SIZE)
        except:
            font = ImageFont.load_default()
    
    draw.multiline_text(
        (50, 50),
        lyrics,
        fill=config.FONT_COLOR,
        font=font,
    )
    
    img.save(config.OUTPUT_FILENAME)
    print(f"Imagen generada: {config.OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()
    # Test simple: Ingrese "Artista - Título"
    print(fetch_lyrics("Coldplay - Yellow"))