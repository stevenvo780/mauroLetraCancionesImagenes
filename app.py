from PIL import Image, ImageDraw, ImageFont
import os
import config
import llm_lyrics
import llm_image

def main():
    song_title = input("Ingrese el título de la canción: ")
    lyrics = llm_lyrics.fetch_lyrics(song_title)
    print("Letra obtenida:")
    print(lyrics)

    img_path = llm_image.generate_image_from_lyrics(lyrics)
    if img_path:
        print(f"Imagen generada por modelo local: {img_path}")
    else:
        print("No se pudo generar la imagen con el modelo local.")

    with open("lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)

    local_img = Image.new(
        "RGB",
        (config.IMAGE_WIDTH, config.IMAGE_HEIGHT),
        color=config.BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(local_img)

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
        font=font,
        fill=config.FONT_COLOR
    )
    local_img.save(config.OUTPUT_FILENAME)
    print(f"Imagen local guardada como: {config.OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()