# Author: Jan Niklas Kolf, 2020
from face_image_quality import SER_FIQ
import cv2
import os
import logging
import argparse

def main(img_dir, output_dir):
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

    logger.debug("--- SER-FIQ start---")
    logger.debug(f"image directory: {img_dir}")

    sum: int = 0
    square_sum: int = 0
    cnt = 0

    # Sample code of calculating the score of an image
    
    # Create the SER-FIQ Model
    # Choose the GPU, default is 0.
    ser_fiq = SER_FIQ(gpu=0)
        
    for _, _, files in os.walk(img_dir):
        for file in files:
            # Load the test image
            test_img = cv2.imread(os.path.join(img_dir, file))
            
            # Align the image
            aligned_img = ser_fiq.apply_mtcnn(test_img)
            
            # Calculate the quality score of the image
            # T=100 (default) is a good choice
            # Alpha and r parameters can be used to scale your
            # score distribution.
            if aligned_img is None:
                score = 0
            else:
                score = ser_fiq.get_score(aligned_img, T=100)

            sum += score
            square_sum += score * score
            cnt += 1
            
            print(f"{file} score: {score}")
            logger.debug(f"{file} score: {score}")
    
    print("average_score:", sum/cnt)
    print("standard_deviation:", (square_sum/cnt - (sum/cnt)**2)**0.5)
    logger.info(f"ser-fiq average score: {sum/cnt}")
    logger.info(f"ser-fiq standard deviation: {(square_sum/cnt - (sum/cnt)**2)**0.5}")
    logger.debug("--- SER-FIQ end---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SER-FIQ')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)
