from PIL import Image
from torchvision.transforms import transforms
import torch
import os
import numpy as np

OUTPUT_DIR = "visualize_noise/output/threshold200/"
CLEAN_FILE_PATH = "/home/acf15469mn/repogitries/Anti-DreamBooth/data/vggface2_light/n000187/setB/0015_01.jpg"
ANTI_FILE_PATH = "/groups/gcc50494/home/onikubo/light_experiment/high_pass_madb_init_clean_5e-3_10e-1_with_threshold_160_50step/images/n000187/adversarial/50_noise_0015_01.png"
FILTERED_FILE_PATH = "./output/threshold200.png"
to_tensor = transforms.ToTensor()
to_image = transforms.ToPILImage()

def main():
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    torch.set_printoptions(edgeitems=1000)
    img_clean = to_tensor(Image.open(CLEAN_FILE_PATH))
    img_anti = to_tensor(Image.open(ANTI_FILE_PATH))
    anti_noise = img_anti - img_clean

    one_tensor = torch.ones_like(img_clean)
    anti_noise = one_tensor - np.abs(anti_noise)

    img_clean_emphasize = anti_noise * 3

    to_image(img_clean_emphasize).save(OUTPUT_DIR + "loss.png")


if __name__ == "__main__":
    main()