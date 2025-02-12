import openai
import config
import os
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch

openai.api_key = "YOUR_API_KEY"

def generate_image_from_lyrics(lyrics: str) -> str:
    prompt = f"Create an artistic image based on the following lyrics: {lyrics}"
    try:
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        image = pipe(prompt).images[0]
        image_path = "sd_output.png"
        image.save(image_path)
        return image_path
    except Exception as e:
        print("Error al generar la imagen:", e)
        return ""

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
        font=font,
        fill=config.FONT_COLOR
    )

    img.save(config.OUTPUT_FILENAME)
    print(f"Imagen generada: {config.OUTPUT_FILENAME}")

    # Generar imagen con LLM o API generativa
    image_url = generate_image_from_lyrics(lyrics)
    if image_url:
        print(f"Imagen generada por LLM: {image_url}")
    else:
        print("No se pudo generar la imagen con LLM")

if __name__ == "__main__":
    main()