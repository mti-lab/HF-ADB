import cv2
import cv2.quality as quality
import os
import logging
import argparse

def main(img_dir, output_dir):
    model_path = "models/brisque/brisque_model_live.yml"
    range_path = "models/brisque/brisque_range_live.yml"

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

    logger.debug("BRISQUE start")

    logger.debug(f"image directory: {img_dir}")

    sum = 0
    square_sum = 0
    cnt = 0

    for _, _, files in os.walk(img_dir):
        for file in files:
            img = cv2.imread(os.path.join(img_dir, file), 1)

            score = quality.QualityBRISQUE_compute(img, model_path, range_path)

            sum += score[0]
            square_sum += score[0] * score[0]
            cnt += 1

            print(file, "score:", score)
            logger.debug(f"{file} score: {score}")

    print("brisque average score:", sum/cnt)
    print("brisque standard deviation:", (square_sum/cnt - (sum/cnt)**2)**0.5)
    logger.info(f"brisque average score: {sum/cnt}")
    logger.info(f"brisque standard deviation: {(square_sum/cnt - (sum/cnt)**2)**0.5}")

    logger.debug("BRISQUE end")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BRISQUE')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)