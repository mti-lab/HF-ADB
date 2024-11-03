export INSTANCE_DIR=${INSTANCE_DIR:-"/home/acf15469mn/repogitries/Anti-DreamBooth/utils/output/gabol_mask_2e-1"}
export DREAMBOOTH_OUTPUT_DIR=${DREAMBOOTH_OUTPUT_DIR:-"/groups/gcc50494/home/onikubo/outputs/demo_experiments/crop_gabor_2e-1/DREAMBOOTH"}
export PROMPT=${PROMPT:-"a photo of sks person"}
export MODEL_PATH=${MODEL_PATH:-"./models/stable-diffusion/stable-diffusion-2-1-base"}
export CLASS_DIR=${CLASS_DIR:-"data/class-person"}
export INSTANCE_PROMPT=${INSTANCE_PROMPT:-"a photo of sks person"}
export CLASS_PROMPT=${CLASS_PROMPT:-"a photo of person"}
export SRC_DIR=${SRC_DIR:-"/repogitries/202403_onikubo"}

cd
source .bashrc
cd $SRC_DIR
conda activate anti-dreambooth

accelerate launch utils/dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_PATH  \
  --enable_xformers_memory_efficient_attention \
  --train_text_encoder \
  --instance_data_dir=$INSTANCE_DIR \
  --class_data_dir=$CLASS_DIR \
  --output_dir=$DREAMBOOTH_OUTPUT_DIR \
  --with_prior_preservation \
  --prior_loss_weight=1.0 \
  --instance_prompt="$INSTANCE_PROMPT" \
  --class_prompt="$CLASS_PROMPT" \
  --inference_prompt="$PROMPT" \
  --resolution=512 \
  --train_batch_size=2 \
  --gradient_accumulation_steps=1 \
  --learning_rate=5e-7 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --num_class_images=200 \
  --max_train_steps=1000 \
  --checkpointing_steps=1000 \
  --center_crop \
  --mixed_precision=bf16 \
  --prior_generation_precision=bf16 \
  --sample_batch_size=8