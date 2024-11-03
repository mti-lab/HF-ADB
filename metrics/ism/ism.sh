export IMAGE_DIR=${IMAGE_DIR:-"outputs/anti_dreambooth_output/beard_man_with_ASPL/n000050_DREAMBOOTH/checkpoint-1000/dreambooth/a_photo_of_sks_person"}
export REFERENCE_DIR=${REFERENCE_DIR:-"data/vggface2/n000050/setA"}
export OUTPUT_PATH=${OUTPUT_PATH:-"metrics/ism/output.log"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}

cd
source .bashrc
cd $SRC_DIR
conda activate ism

python metrics/ism/ism.py --img_dir $IMAGE_DIR --ref_dir $REFERENCE_DIR --output_dir $OUTPUT_PATH
