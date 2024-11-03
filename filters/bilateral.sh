export IMAGE_DIR=${IMAGE_DIR:-"data/strong_noise_50"}
export OUTPUT_DIR=${OUTPUT_DIR:-"filter/output/bilateral"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}


cd
source .bashrc
cd $SRC_DIR
conda activate bilateral

python filters/bilateral.py --img_dir $IMAGE_DIR --output_dir $OUTPUT_DIR/bilateral
