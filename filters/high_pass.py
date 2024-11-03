import cv2
import os
import argparse
import numpy as np

K_SIZE = 10
SIGMA = 4.0

kernel_high_pass = np.array([
                            [-1, -1, -1],
                            [-1,  8, -1],
                            [-1, -1, -1]
                            ], np.float32)


def make_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def main(img_dir, output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for _, _, files in os.walk(img_dir):
        for file in files:
            img = cv2.imread(os.path.join(img_dir, file), cv2.IMREAD_GRAYSCALE)
            filtered_img = cv2.filter2D(img, -1, kernel_high_pass)
            filtered_img = cv2.bitwise_not(filtered_img)
            cv2.imwrite(os.path.join(output_dir, ''.join(file.split('.')[:-1]) + '.png'), filtered_img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BILATERAL')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir)