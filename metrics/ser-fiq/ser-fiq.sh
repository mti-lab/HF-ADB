export IMAGE_DIR=${IMAGE_DIR:-"outputs/anti_dreambooth_output/beard_man_with_ASPL/n000050_DREAMBOOTH/checkpoint-1000/dreambooth/a_photo_of_sks_person"}
export OUTPUT_PATH=${OUTPUT_PATH:-"metrics/ser-fiq/output.log"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}

cd
source .bashrc
cd $SRC_DIR

module load cuda/11.7/11.7.1
module load cudnn/8.7/8.7.0
module load nccl/2.13/2.13.4-1

conda activate ser-fiq

python metrics/ser-fiq/ser-fiq.py --img_dir $IMAGE_DIR --output_dir $OUTPUT_PATH
