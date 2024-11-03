export ALPHA="5e-3"
export NOISE_LEVEL_IN_MASK="5e-1"
export NOISE_LEVEL_OUT_MASK="1e-2"
export MASK_AREA="3e-2"
export STEP="50"
export EXPERIMENT_NAME="demo"
export MODEL_PATH="./models/stable-diffusion/stable-diffusion-2-1-base"
export CLASS_DIR="./data/class_image"
export INSTANCE_DIR="./data/demo"
export HOME_DIR="./output/$EXPERIMENT_NAME"
export PROMPT="a photo of sks person"
export PROMPT_DIR="a_photo_of_sks_person"
export MIXED_PRECISION="fp16"
export SRC_DIR="./HF-ADB"

cd
source .bashrc
cd $SRC_DIR

CREATE_MASK=true
DO_ATTACK=true
APPLY_BILATERAL_FILTER=false
APPLY_DIFFPURE=false
TRAIN_DREAMBOOTH=true
INPUT_EVALUATION=false
INPUT_SUMMERIZATIO=false
OUTPUT_EVALUATION=false
OUTPUT_SUMMERIZATION=false



for dir in "$INSTANCE_DIR"/*; do
    export SAMPLE_ID=$(basename "$dir")
    export CLEAN_TRAIN_DIR="$dir"/setA
    export CLEAN_ADV_DIR="$dir"/setB
    export MASK_DIR="$HOME_DIR/masks/$SAMPLE_ID"/

    mkdir -p $MASK_DIR

    # create mask
    if $CREATE_MASK; then
        export IMAGE_DIR=$CLEAN_ADV_DIR
        export OUTPUT_DIR=$MASK_DIR
        bash filters/high_pass.sh
        export IMAGE_DIR=$MASK_DIR
        bash utils/threshold_by_area.sh
    fi


    export OUTPUT_DIR=$HOME_DIR/images/$SAMPLE_ID

    # adversary attack
    if $DO_ATTACK; then
        bash attacks/hfadb.sh
        wait $!
    fi

    # apply filter
    export IMAGE_DIR=$OUTPUT_DIR/adversarial
    if $APPLY_BILATERAL_FILTER; then
        bash filters/bilateral.sh
        wait $!
    fi

    if $APPLY_DIFFPURE; then
        bash filters/diffpure.sh
        wait $!
    fi

    # input evaluation
    if $INPUT_EVALUATION; then
        for method in "$HOME_DIR/images/$SAMPLE_ID"/*; do
            mkdir -p "$HOME_DIR/evaluation/inputs/$(basename "$method")/$SAMPLE_ID/"

            export IMAGE_DIR="$method"
            export REFERENCE_DIR="$dir"/setC
            export OUTPUT_PATH="$HOME_DIR/evaluation/inputs/$(basename "$method")/$SAMPLE_ID/"

            echo $method

                bash metrics/fdfr/fdfr.sh
                bash metrics/ism/ism.sh
                bash metrics/ser-fiq/ser-fiq.sh
                bash metrics/brisque/brisque.sh
                bash metrics/l_p/l_p.sh
                wait $!
        done
    fi

    # train DreamBooth
    export OUTPUT_DIR=$HOME_DIR
    for method in "$OUTPUT_DIR/images/$SAMPLE_ID"/*; do
        export INSTANCE_DIR=$method
        export DREAMBOOTH_OUTPUT_DIR=$OUTPUT_DIR/outputs/$SAMPLE_ID/$(basename "$method")
        if $TRAIN_DREAMBOOTH; then
            bash utils/dreambooth.sh
            wait $!
            cp $DREAMBOOTH_OUTPUT_DIR/checkpoint-1000/dreambooth/$PROMPT_DIR/* $DREAMBOOTH_OUTPUT_DIR
            rm -r $DREAMBOOTH_OUTPUT_DIR/checkpoint-1000
            rm -r $DREAMBOOTH_OUTPUT_DIR/logs
        fi
    done

    # output evaluation
    if $OUTPUT_EVALUATION; then
        for method in "$HOME_DIR/outputs/$SAMPLE_ID"/*; do
            mkdir -p "$HOME_DIR/evaluation/outputs/$(basename "$method")/$SAMPLE_ID"

            export IMAGE_DIR="$method"
            export REFERENCE_DIR="$dir"/setC
            export OUTPUT_PATH="$HOME_DIR/evaluation/outputs/$(basename "$method")/$SAMPLE_ID"
                bash metrics/fdfr/fdfr.sh
                bash metrics/ism/ism.sh
                bash metrics/ser-fiq/ser-fiq.sh
                bash metrics/brisque/brisque.sh
                wait $!
        done
    fi
done

# input summerization
export LOG_DIR=$HOME_DIR/evaluation/inputs
export OUTPUT_PATH=$HOME_DIR/evaluation/inputs
export IS_INPUT="true"
if $INPUT_SUMMERIZATION; then
    bash metrics/summerize.sh
fi

# output summerization
export IS_INPUT="false"
export LOG_DIR=$HOME_DIR/evaluation/outputs
export OUTPUT_PATH=$HOME_DIR/evaluation/outputs
if $OUTPUT_SUMMERIZATION; then
    bash metrics/summerize.sh
fi
