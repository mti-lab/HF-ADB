import cv2
import os

FILE_DIR = "data/onikubo/original/"
OUTPUT_DIR = "data/onikubo/"

def main():
    for _, _, files in os.walk(FILE_DIR):
        for file in files:
            img = cv2.imread(FILE_DIR + file)
            resized_img = cv2.resize(img, (512, 512))

            cv2.imwrite(OUTPUT_DIR + file, resized_img)

if __name__ == "__main__":
    main()