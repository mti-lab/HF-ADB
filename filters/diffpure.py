from PIL import Image
import os
from diffusers import UNet2DModel, DDPMScheduler
import torch
import torchvision.transforms as transforms
import argparse

STEP_NUM = 50
device = "cuda"

to_tensor = transforms.ToTensor()
to_image = transforms.ToPILImage()
    
def ddpm(image: Image, unet: UNet2DModel, scheduler: DDPMScheduler) -> Image:
    img = to_tensor(image)
    img = (img - 0.5) * 2

    # add noise
    noise =  torch.randn_like(img) 
    img = scheduler.add_noise(img, noise, scheduler.timesteps[1000-STEP_NUM]).unsqueeze(0).to(device)

    with torch.no_grad():
        for t in scheduler.timesteps[1000-STEP_NUM:1000]:
            # 1. predict noise model_output
            model_output = unet(img, t).sample

            # 2. compute previous image: x_t -> x_t-1
            img = scheduler.step(model_output, t, img).prev_sample

    img = (img / 2 + 0.5).clamp(0, 1)
    img = img.cpu()
    img = to_image(img[0])

    return img

def main(img_dir, output_dir):
    unet = UNet2DModel.from_pretrained("google/ddpm-celebahq-256")
    scheduler = DDPMScheduler.from_pretrained("google/ddpm-celebahq-256")
    unet.to(device)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        
    for _, _, files in os.walk(img_dir):
        for file in files:
            img = Image.open(os.path.join(img_dir, file)).convert('RGB')
            filtered_img = ddpm(img, unet, scheduler)
            filtered_img.save(os.path.join(output_dir, file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DiffPure')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)