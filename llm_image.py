import os
import config
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch
from local_model import LocalModel

local_model = LocalModel()

def generate_image_from_lyrics(lyrics: str) -> str:
    creative_prompt = local_model.get_response("A partir de la siguiente letra, genera una descripción creativa para una imagen: " + lyrics)
    print("Prompt creativo generado:", creative_prompt)
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32, safety_checker=None)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        image = pipe(creative_prompt).images[0]
        image_path = os.path.join(output_folder, "sd_output.png")
        image.save(image_path)
        return image_path
    except Exception as e:
        print("Error al generar la imagen:", e)
        return ""

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
    draw.multiline_text((50, 50), lyrics, font=font, fill=config.FONT_COLOR)
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    local_out = os.path.join(output_folder, config.OUTPUT_FILENAME)
    img.save(local_out)
    print("Imagen generada localmente:", local_out)
    image_path = generate_image_from_lyrics(lyrics)
    if image_path:
        print("Imagen generada por modelo local:", image_path)
    else:
        print("No se pudo generar la imagen con el modelo local.")

if __name__ == "__main__":
    main()