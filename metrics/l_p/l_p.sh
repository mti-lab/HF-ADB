export IMAGE_DIR=${IMAGE_DIR:-"/groups/gcc50494/home/onikubo/main_experiment/anti_dreambooth_1e-1/images/n000033/adversarial"}
export CLEAN_ADV_DIR=${CLEAN_ADV_DIR:-"/groups/gcc50494/home/onikubo/main_experiment/anti_dreambooth_1e-1/images/n000033/clean"}
export OUTPUT_PATH=${OUTPUT_PATH:-"metrics/l_p/output.log"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}

cd
source .bashrc
cd $SRC_DIR
conda activate l_p

python metrics/l_p/l_p.py --clean_img_dir $CLEAN_ADV_DIR --adv_img_dir $IMAGE_DIR --output_dir $OUTPUT_PATH
