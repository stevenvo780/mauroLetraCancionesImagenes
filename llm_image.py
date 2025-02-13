import os
import config
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch
from local_model import LocalModel

local_model = LocalModel()

def generate_image_from_lyrics(lyrics: str) -> str:
    prompt_input = (
        "Convierte la siguiente letra en un prompt creativo para generar una imagen digital "
        "de alta calidad. Emplea un lenguaje descriptivo, incluyendo detalles artísticos, "
        "ambientación cinematográfica, composición equilibrada y colores vibrantes. Letra: " + 
        lyrics
    )
    creative_prompt = local_model.get_response(prompt_input)
    print("Prompt creativo generado:", creative_prompt)
    if not creative_prompt:
        print("El modelo no devolvió un prompt válido.")
        return ""
    
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        # Usar modelo base más ligero y configuración simplificada
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        
        # Generar imagen con parámetros explícitos
        image = pipe(
            prompt=creative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5
        ).images[0]
        
        image_path = os.path.join(output_folder, "sd_output.png")
        image.save(image_path)
        return image_path
    except Exception as e:
        print("Error al generar la imagen:", e)
        print("Detalles del error:", str(e))
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