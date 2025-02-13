import os
import config
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch
from local_model import LocalModel

# Instanciar modelo local para generación de prompt creativo
local_model = LocalModel()

def generate_image_from_lyrics(lyrics: str) -> str:
    # Generar una descripción creativa a partir de la letra
    creative_prompt = local_model.get_response(
        "A partir de la siguiente letra, genera una descripción creativa para una imagen: " + lyrics
    )
    print("Prompt creativo generado:", creative_prompt)
    try:
        # Cargar modelo sin el parámetro revision para evitar errores; 
        # se usa torch_dtype para obtener FP32 y safety_checker desactivado
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float32,
            safety_checker=None  # Opcional: desactivar safety_checker
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        image = pipe(creative_prompt).images[0]
        image_path = "sd_output.png"
        image.save(image_path)
        return image_path
    except Exception as e:
        print("Error al generar la imagen:", e)
        return ""

def main():
    with open("lyrics.txt", "r", encoding="utf-8") as f:
        lyrics = f.read()

    # Imagen local con Pillow (opcional)
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
    print(f"Imagen generada localmente: {config.OUTPUT_FILENAME}")

    # Generar imagen con descripción creativa generada por LLM local
    image_path = generate_image_from_lyrics(lyrics)
    if image_path:
        print(f"Imagen generada por modelo local: {image_path}")
    else:
        print("No se pudo generar la imagen con el modelo local.")

if __name__ == "__main__":
    main()