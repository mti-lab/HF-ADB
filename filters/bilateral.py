import cv2
import os
import argparse

def make_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def main(img_dir, output_dir):
    os.makedirs(output_dir)

    for _, _, files in os.walk(img_dir):
        for file in files:
            img = cv2.imread(os.path.join(img_dir, file), cv2.IMREAD_COLOR)
            filtered_img = cv2.bilateralFilter(img, 9, 50, 50)
            cv2.imwrite(os.path.join(output_dir, file), filtered_img)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BILATERAL')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)