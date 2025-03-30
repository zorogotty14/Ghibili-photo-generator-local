import torch
from diffusers import StableDiffusionImg2ImgPipeline
import gradio as gr
from PIL import Image
import time
import os

# Check for GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

# Load the model with GPU support
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=dtype
).to(device)

# Optional: Load LoRA if you have one
pipe.load_lora_weights("path_to_ghibli_lora/ghibli_lora.safetensors")

# Ensure output folder exists
os.makedirs("generated_images", exist_ok=True)

def generate_ghibli_style(input_image):
    prompt = "ghibli style, anime background, dreamy, vibrant colors"
    
    # Resize image to 512x512 (recommended by Stable Diffusion)
    input_image = input_image.resize((512, 512))
    
    result = pipe(
        prompt=prompt,
        image=input_image,
        strength=0.7,
        guidance_scale=8.5,
        num_inference_steps=30
    ).images[0]
    
    # Save the result with timestamp
    filename = f"generated_images/ghibli_{int(time.time())}.png"
    result.save(filename)
    
    return result

# Gradio Interface
gr.Interface(
    fn=generate_ghibli_style,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(),
    title="Ghibli Style Image Generator (GPU)",
    description="Upload an image and transform it into Ghibli-style anime art. The result will also be saved locally."
).launch()
