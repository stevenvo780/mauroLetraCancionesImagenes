import os
import uuid
import config
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch

def generate_image_from_lyrics(creative_prompt: str, steps: int = 20, guidance: float = 8.0, gen_width: int = None, gen_height: int = None, callback=None) -> str:
    if not creative_prompt:
        return ""
    print(f"Prompt generado: {creative_prompt}")
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    device = "cpu"
    try:
        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        pipe.enable_attention_slicing()
        pipe = pipe.to(device)
        pipe_args = {
            "prompt": creative_prompt,
            "num_inference_steps": steps,
            "guidance_scale": guidance
        }
        if gen_width and gen_height:
            pipe_args["width"] = gen_width
            pipe_args["height"] = gen_height
        if callback:
            pipe_args["callback"] = callback
            pipe_args["callback_steps"] = 1
        image = pipe(**pipe_args).images[0]
        unique_id = uuid.uuid4().hex
        image_filename = f"sd_output_{unique_id}.png"
        image_path = os.path.join(output_folder, image_filename)
        image.save(image_path)
        print("Image generated:", image_path, flush=True)
        return image_path
    except Exception as e:
        print("Error generating image:", e, flush=True)
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
        except Exception:
            font = ImageFont.load_default()
    draw.multiline_text((50, 50), lyrics, font=font, fill=config.FONT_COLOR)
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    local_out = os.path.join(output_folder, config.OUTPUT_FILENAME)
    img.save(local_out)
    print("Local image generated:", local_out, flush=True)
    creative_prompt = generate_creative_prompt(lyrics)
    image_path = generate_image_from_lyrics(creative_prompt)
    if image_path:
        print("Image generated by model:", image_path, flush=True)
    else:
        print("Failed to generate image with the model.", flush=True)

if __name__ == "__main__":
    main()
