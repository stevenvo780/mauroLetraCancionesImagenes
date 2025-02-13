from PIL import Image, ImageDraw, ImageFont
import os
import config
import lyrics
import llm_image

def main():
    song_title = input("Ingrese el título de la canción: ")
    lyric_text = lyrics.fetch_lyrics(song_title)
    print("Letra obtenida:")
    print(lyric_text)

    img_path = llm_image.generate_image_from_lyrics(lyric_text)
    if img_path:
        print("Imagen generada por modelo local:", img_path)
    else:
        print("No se pudo generar la imagen con el modelo local.")

    with open("lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyric_text)

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
        lyric_text,
        font=font,
        fill=config.FONT_COLOR
    )
    local_output = os.path.join(output_folder, config.OUTPUT_FILENAME)
    local_img.save(local_output)
    print("Imagen local guardada como:", local_output)

if __name__ == "__main__":
    main()