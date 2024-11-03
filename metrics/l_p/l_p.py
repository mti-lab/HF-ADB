import os
import logging
import argparse
import cv2
import numpy as np

def l_p(x, y, p):
    im1 = cv2.imread(x)
    im2 = cv2.imread(y)
    im3 = im1-im2
    value = np.sum(im3**p) ** (1/p)
    return value

def l_0(x, y):
    im1 = cv2.imread(x)
    im2 = cv2.imread(y)
    value = np.sum((im1-im2)**0)
    return value

def calc_norm(x, y):
    im1 = cv2.imread(x)
    im2 = cv2.imread(y)
    
    return {"l_1": cv2.norm(im1, im2, cv2.NORM_L1), "l_2": cv2.norm(im1, im2, cv2.NORM_L2)}

def main(clean_img_dir, adv_img_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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

    logger.debug("---l_p start---")
    logger.debug(f"image directory: {adv_img_dir}")
    logger.debug(f"clean image directory: {clean_img_dir}")
    print(f"image directory: {adv_img_dir}")
    print(f"clean image directory: {clean_img_dir}")

    l_1_sum = 0
    l_2_sum = 0
    cnt = 0
    for _, _, files in os.walk(clean_img_dir):
        for file in files:
            cnt += 1
            clean_path = os.path.join(clean_img_dir, file)
            adv_path = os.path.join(adv_img_dir, "50_noise_" + "".join(file.split(".")[:-1]) + ".png")
            print(clean_path, adv_path)
            score = calc_norm(clean_path, adv_path)
            logger.debug(f"{file} score: {str(score)}")
            l_1_sum += score["l_1"]
            l_2_sum += score["l_2"]

    print(f"l_1 average score: {l_1_sum/cnt}")
    print(f"l_2 average score: {l_2_sum/cnt}")
    logger.info(f"l_1 average score: {l_1_sum/cnt}")
    logger.info(f"l_2 average score: {l_2_sum/cnt}")

    logger.debug("---l_p end---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FDFR')
    parser.add_argument('--clean_img_dir', type=str, default=None)
    parser.add_argument('--adv_img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.clean_img_dir, args.adv_img_dir, args.output_dir)
