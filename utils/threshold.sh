export IMAGE_DIR=${IMAGE_DIR:-"data/strong_noise_50"}
export OUTPUT_DIR=${OUTPUT_DIR:-"filter/output/"}
export THRESHOLD=${THRESHOLD:-"180"}

cd
source .bashrc
cd $SRC_DIR
conda activate base

python utils/threshold.py --img_dir $IMAGE_DIR --output_dir $OUTPUT_DIR --threshold $THRESHOLD
