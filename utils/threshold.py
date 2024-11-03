import argparse
import cv2
import os

def main(mask_dir, output_dir, threshold):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for _, _, files in os.walk(mask_dir):
        for file in files:
            img = cv2.imread(os.path.join(mask_dir, file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
            cv2.imwrite(os.path.join(output_dir, ''.join(file.split('.')[:-1]) + '.png'), img_thresh)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='threshold')
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--output_dir', type=str, default=None)
    parser.add_argument('--threshold', type=int, default=128)
    args = parser.parse_args()
    main(args.img_dir, args.output_dir, args.threshold)