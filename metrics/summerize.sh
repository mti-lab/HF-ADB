#!/bin/bash

#$-l rt_G.small=1
#$-l h_rt=0:30:00
#$-j y

export EXPERIMENT_NAME=${EXPERIMENT_NAME:-"high_pass_madb_init_clean_5e-3_2e-1_with_threshold_160_50step"}
export LOG_DIR=${LOG_DIR:-"/groups/gcc50494/home/onikubo/main_experiment/high_pass_madb_init_clean_5e-3_2e-1_with_threshold_160_50step/inputs"}
export OUTPUT_PATH=${OUTPUT_PATH:-"/groups/gcc50494/home/onikubo/main_experiment/high_pass_madb_init_clean_5e-3_2e-1_with_threshold_160_50step/inputs"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}
export IS_INPUT=${IS_INPUT:-"false"}

cd
source .bashrc
cd $SRC_DIR

conda activate base

python metrics/summerize.py --experiment_name $EXPERIMENT_NAME --log_dir $LOG_DIR --output_dir $OUTPUT_PATH --is_input $IS_INPUT