import os
import uuid
from diffusers import StableDiffusionPipeline
import torch

def generate_image_from_lyrics(creative_prompt: str, steps: int = 20, guidance: float = 8.0, gen_width: int = None, gen_height: int = None, callback=None) -> str:
    if not creative_prompt:
        return ""
    print(f"Prompt generado: {creative_prompt}")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_folder = os.path.join(base_dir, "output")
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