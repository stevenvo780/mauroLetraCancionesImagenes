from PIL import Image, ImageDraw, ImageFont
import os
import config
import lyrics
import llm_image
from local_model import LocalModel

def main():
    song_title = input("Ingrese el título de la canción: ")
    lyric_text = lyrics.fetch_lyrics(song_title)
    print("Letra obtenida:")
    print(lyric_text)
    
    # Generar imagen con modelo local (SDXL)
    img_path = llm_image.generate_image_from_lyrics(lyric_text)
    if img_path:
        print("Imagen generada por modelo local:", img_path)
    else:
        print("No se pudo generar la imagen con el modelo local.")

    with open("lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyric_text)

    # Obtener versión creativa de la letra para imprimirla en la imagen
    local_model = LocalModel()
    creative_text = local_model.get_response(
        "Convierte la siguiente letra en una descripción poética y evocadora para una imagen: " + lyric_text
    )
    print("Texto creativo para imagen:", creative_text)

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    local_img = Image.new("RGB", (config.IMAGE_WIDTH, config.IMAGE_HEIGHT), color=config.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(local_img)

    font_path = config.FONT_PATH
    if not os.path.exists(font_path):
        font = ImageFont.load_default()
    else:
        try:
            font = ImageFont.truetype(font_path, config.FONT_SIZE)
        except:
            font = ImageFont.load_default()

    draw.multiline_text((50, 50), creative_text, font=font, fill=config.FONT_COLOR)
    local_output = os.path.join(output_folder, config.OUTPUT_FILENAME)
    local_img.save(local_output)
    print("Imagen local guardada como:", local_output)

if __name__ == "__main__":
    main()