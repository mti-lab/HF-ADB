import argparse
import os
import logging
from statistics import mean, variance

import cv2
import numpy as np
import torch

from backbones import get_model

WEIGHT = "metrics/ism/model/backbone.pth"
MODEL = "r100"

def load_img(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (112, 112))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (2, 0, 1))
    img = torch.from_numpy(img).unsqueeze(0).float()
    img.div_(255).sub_(0.5).div_(0.5)
    return img

@torch.no_grad()
def calc_emb(model, path):
    img = load_img(path)
    emb = model(img).numpy()
    return emb
            
def cos_sim(v1, v2):
    return np.tensordot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main(img_dir, ref_dir, output_dir):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    detaile_handler = logging.FileHandler(os.path.join(output_dir, "details.log"))
    detaile_handler.setFormatter(formatter)
    detaile_handler.setLevel(logging.DEBUG)

    evalation_handler = logging.FileHandler(os.path.join(output_dir, "evaluation.log"))
    evalation_handler.setFormatter(formatter)
    evalation_handler.setLevel(logging.INFO)

    logger.addHandler(detaile_handler)
    logger.addHandler(evalation_handler)

    logger.debug("---ISM start---")
    logger.debug(f"image directory: {img_dir}")

    model = get_model(MODEL, fp16=False)
    model.load_state_dict(torch.load(WEIGHT))
    model.eval()

    # inference embeddings of reference images
    ref_embs = []
    for _, _, files in os.walk(ref_dir):
        for file in files:
            emb = calc_emb(model, os.path.join(ref_dir, file))
            ref_embs.append(emb)

    sum = 0
    square_sum = 0
    cnt = 0

    for _, _, files in os.walk(img_dir):
        for file in files:
            img_emb = calc_emb(model, os.path.join(img_dir, file))
            score = mean([cos_sim(img_emb, ref_emb) for ref_emb in ref_embs])
            print(f"{file} score: {score}")
            logger.debug(f"{file} score: {score}")
            sum += score
            square_sum += score ** 2
            cnt += 1
    ave_score = sum / cnt
    deviation_score = np.sqrt(square_sum / cnt - ave_score ** 2)
    print(f"ism average score: {ave_score}")
    print(f"ism standard deviation: {deviation_score}")
    logger.info(f"ism average score: {ave_score}")
    logger.info(f"ism standard deviation: {deviation_score}")
    logger.debug("---ISM end---")
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ISM')
    parser.add_argument('--network', type=str, default='r100', help='backbone network')
    parser.add_argument('--weight', type=str, default='')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--ref_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.ref_dir, args.output_dir)
