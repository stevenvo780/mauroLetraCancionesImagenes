import requests
import config
import os
from PIL import Image, ImageDraw, ImageFont

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

def main():
    with open("lyrics.txt", "r", encoding="utf-8") as f:
        lyrics = f.read()
    img = Image.new("RGB", (config.IMAGE_WIDTH, config.IMAGE_HEIGHT), color=config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    font_path = config.FONT_PATH
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        try:
            font = ImageFont.truetype(font_path, config.FONT_SIZE)
        except:
            font = ImageFont.load_default()
    draw.multiline_text((50, 50), lyrics, fill=config.FONT_COLOR, font=font)
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    local_out = os.path.join(output_folder, config.OUTPUT_FILENAME)
    img.save(local_out)
    print("Imagen generada:", local_out)

if __name__ == "__main__":
    main()
    print(fetch_lyrics("Coldplay - Yellow"))