# High-Frequency Anti-DreamBooth: Robust Defense against Personalized Image Synthesis

## Environment

1. Create virtual environment with conda

```
conda env create -n {env_name} --file env/env-{env_name}.txt
```

necessary
- `env/env-anti-dreambooth.yaml`

optional (for evaluation)
- `env/env-bilateral.yaml`
- `env/env-brisque.yaml`
- `env/env-diffpure.yaml`
- `env/env-fdfr.yaml`
- `env/env-ism.yaml`
- `env/env-l_p.yaml`
- `env/env-ser-fiq.yaml`

2. Install PyTorch manually

```
conda activate anti-dreambooth
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
```

3. Download Stable Diffusion model from following url, and put it in `model/`

- [Stable Diffsion](https://huggingface.co/stabilityai/stable-diffusion-2-1)

↓ One of the easiest way of downloading Stable Diffusion using python.

```
import huggingface_hub
 
model_id = "stabilityai/stable-diffusion-2-1-base"
local_dir = "models/stable-diffusion/stable-diffusion-2-1-base"
huggingface_hub.snapshot_download(model_id, local_dir=local_dir, local_dir_use_symlinks=False)
```

## How to run code

We used NVIDIA A100 SXM.

1. Set experiment configurations on `job_scripts/hfadb.sh`

- ALPHA: The amount of noise added in each step
- NOISE_LEVEL_IN_MASK: The maximum amount of noise added on high-frequency area
- NOISE_LEVEL_OUT_MASK: The maximum amount of noise added on low-frequency area
- MASK_AREA: The ratio of high-frequency area
- STEP: The number of steps to add noise
- EXPERIMENT_NAME: Arbitrary experiment name
- CLASS_DIR: Direntory where you put class image for Stable Diffusion
- INSTANCE_DIR: Directory of sample images
- HOME_DIR: Directory of outputs
- PROMPT: Prompt for generation
- PROMPT_DIR: Replace `' '` of `PROMPT` with `'_'`
- SRC_DIR: Root directory of the source code

2. Run this command on terminal

```
bash ./job_scripts/hfadb.sh
```

## Reference
- [arxiv](https://arxiv.org/abs/2409.08167)
- bibtex
```
@inproceedings{onikubo2024high,
  title={High-Frequency Anti-DreamBooth: Robust Defense against Personalized Image Synthesis},
  author={Onikubo, Takuto and Matsui, Yusuke},
  booktitle={ECCV 2024 Workshop The Dark Side of Generative AIs and Beyond}
}
```
