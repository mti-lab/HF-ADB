export EXPERIMENT_NAME=${EXPERIMENT_NAME:-"pgd_eps_1e-1_ASPL"}
export MODEL_PATH=${MODEL_PATH:-"./models/stable-diffusion/stable-diffusion-2-1-base"}
export CLASS_DIR=${CLASS_DIR:-"data/class-person"}
export CLEAN_TRAIN_DIR=${CLEAN_TRAIN_DIR:-"data/vggface2/n000050/setA"}
export CLEAN_ADV_DIR=${CLEAN_ADV_DIR:-"data/vggface2/n000050/setB"}
export OUTPUT_DIR=${OUTPUT_DIR:-"/groups/gcc50494/home/onikubo/outputs/$EXPERIMENT_NAME/ADVERSARIAL"}
export MASK_DIR=${MASK_DIR:-"data/mask"}
export NOISE_LEVEL_IN_MASK=${NOISE_LEVEL_IN_MASK:-"1e-1"}
export NOISE_LEVEL_OUT_MASK=${NOISE_LEVEL_OUT_MASK:-"1e-2"}
export ALPHA=${ALPHA:-"5e-3"}
export STEP=${STEP:-"50"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}

# ------------------------- Train ASPL on set B -------------------------
cd
source .bashrc
cd $SRC_DIR
mkdir -p $OUTPUT_DIR/adversarial
conda activate anti-dreambooth

accelerate launch attacks/hfadb.py \
  --pretrained_model_name_or_path=$MODEL_PATH  \
  --enable_xformers_memory_efficient_attention \
  --instance_data_dir_for_train=$CLEAN_TRAIN_DIR \
  --instance_data_dir_for_mask=$MASK_DIR \
  --instance_data_dir_for_adversarial=$CLEAN_ADV_DIR \
  --instance_prompt="a photo of sks person" \
  --class_data_dir=$CLASS_DIR \
  --num_class_images=200 \
  --class_prompt="a photo of person" \
  --output_dir=$OUTPUT_DIR \
  --center_crop \
  --with_prior_preservation \
  --prior_loss_weight=1.0 \
  --resolution=512 \
  --train_text_encoder \
  --train_batch_size=1 \
  --max_train_steps=$STEP \
  --max_f_train_steps=3 \
  --max_adv_train_steps=6 \
  --checkpointing_iterations=10 \
  --learning_rate=5e-7 \
  --pgd_alpha=$ALPHA \
  --pgd_eps=$NOISE_LEVEL_OUT_MASK \
  --mask_pgd_eps=$NOISE_LEVEL_IN_MASK

cp $OUTPUT_DIR/noise-ckpt/$STEP/* $OUTPUT_DIR/adversarial
rm -r "$OUTPUT_DIR/noise-ckpt"
