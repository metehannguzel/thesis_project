from flask import Flask, request, jsonify 
import torch 
from PIL import Image 
from diffusers import StableDiffusionImg2ImgPipeline 
import io 
import base64 
import json 
from datetime import date 
from xformers.ops import MemoryEfficientAttentionFlashAttentionOp 
app = Flask(_name_) 
 
device = "cuda" 
model_id_or_path = "runwayml/stable-diffusion-v1-5" 
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16) 
pipe = pipe.to(device) 
pipe.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp) 
 
pipe.vae.enable_xformers_memory_efficient_attention(attention_op=None) 
 
with open("prompts.json", "r") as prompt_file: 
    prompts = json.load(prompt_file) 
with open("country_based_prompts.json","r") as country_based_prompt_file: 
    country_based_prompts = json.load(country_based_prompt_file) 
 
def get_prompt_pair_for_today(country): 
    today = date.today().isoformat() 
    country_based_prompt = country_based_prompts.get(country,None) 
    print(country_based_prompt) 
    prompt_pair = country_based_prompt.get(today,None) 
    if prompt_pair is None: 
        prompt_pair = prompts.get(today, None) 
        print(prompt_pair) 
        if prompt_pair is None: 
            return None,None 
    return prompt_pair["prompt"], prompt_pair["negative_prompt"] 
 
@app.route("/") 
def hello(): 
    return "Hello, World!" 
 
@app.route("/process_image", methods=["POST"]) 
def process_image(): 
    try: 
        # Receive the image from the request 
        image_file = request.files["image"] 
        init_image = Image.open(image_file).convert("RGB") 
        init_image = init_image.resize((1024, 1024)) 
        country = request.form["country"] 
        # Get prompt and negative prompt pair for today 
        prompt, negative_prompt = get_prompt_pair_for_today(country) 
 
        if prompt is None or negative_prompt is None: 
            return jsonify({"error": "No prompt pair available for today"}), 400 
 
        # Process the image using the model 
        images = pipe(prompt=prompt, image=init_image, strength=0.8, negative_prompt=negative_prompt, guidance_scale=12).images 
 
        buffered = io.BytesIO() 
        images[0].save(buffered, format="PNG") 
        image_data = base64.b64encode(buffered.getvalue()).decode("utf-8") 
     
        # Return the generated image as a base64 encoded string in the API response 
        return jsonify({"image_data": image_data}) 
 
    except Exception as e: 
        return jsonify({"error": str(e)}), 500 
 
if _name_ == "_main_": 
    app.run(port=5002)