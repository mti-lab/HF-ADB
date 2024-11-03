import argparse
import cv2
import os
import numpy as np

def main(mask_dir, output_dir, mask_area):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for _, _, files in os.walk(mask_dir):
        for file in files:
            img = cv2.imread(os.path.join(mask_dir, file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pixels = []
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    pixels.append([img[i, j], i, j])
            pixels.sort(key=lambda x: x)
            new_img = np.zeros_like(img) + 255
            for i in range(int(len(pixels) * mask_area)):
                new_img[pixels[i][1], pixels[i][2]] = 0
            cv2.imwrite(os.path.join(output_dir, ''.join(file.split('.')[:-1]) + '.png'), new_img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='threshold')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    parser.add_argument('--mask_area', type=float, default=0.2)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir, args.mask_area)