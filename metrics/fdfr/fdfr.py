from retinaface import RetinaFace
import os
import logging
import argparse

def main(img_dir, output_dir):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    detaile_handler = logging.FileHandler(os.path.join(output_dir, "details.log"), mode='w')
    detaile_handler.setFormatter(formatter)
    detaile_handler.setLevel(logging.DEBUG)

    evalation_handler = logging.FileHandler(os.path.join(output_dir, "evaluation.log"), mode='w')
    evalation_handler.setFormatter(formatter)
    evalation_handler.setLevel(logging.INFO)

    logger.addHandler(detaile_handler)
    logger.addHandler(evalation_handler)

    logger.debug("---FDFR start---")
    logger.debug(f"image directory: {img_dir}")

    sum = 0
    square_sum = 0
    cnt = 0
    for _, _, files in os.walk(img_dir):
        for file in files:
            resp = RetinaFace.detect_faces(os.path.join(img_dir, file))
            print(resp)
            logger.debug(f"{file} score: {str(resp)}")
            if(any(resp)): sum += 1
            if(any(resp)): square_sum += 1
            cnt+=1

    print("average score:", sum/cnt)
    print("standard deviation:", (square_sum/cnt - (sum/cnt)**2)**0.5)
    logger.info(f"fdfr average score: {sum/cnt}")
    logger.info(f"fdfr standard deviation: {(square_sum/cnt - (sum/cnt)**2)**0.5}")

    logger.debug("---FDFR end---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FDFR')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)
