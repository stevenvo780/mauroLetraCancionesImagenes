from transformers import pipeline
import config
import os
from PIL import Image, ImageDraw, ImageFont

generator = pipeline("text-generation", model="gpt2")

def fetch_lyrics(song_title: str) -> str:
    prompt = f"Find the full lyrics for the song '{song_title}'. Provide only the lyrics."
    try:
        result = generator(prompt, max_length=500, num_return_sequences=1)
        lyrics = result[0]['generated_text']
        if lyrics.startswith(prompt):
            lyrics = lyrics[len(prompt):].strip()
        return lyrics
    except Exception as e:
        print("Error al obtener la letra:", e)
        return "No lyrics found."

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
        try:
            font = ImageFont.truetype(font_path, config.FONT_SIZE)
        except:
            font = ImageFont.load_default()
    else:
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