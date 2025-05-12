from experimentai_api.configs.settings import (MODEL_WEIGHTS_REPO,
                                               MODEL_WEIGHTS_PATH,
                                               MODEL_WEIGHTS_FILE,
                                               MODEL_WEIGHTS_CONFIG_FILE,
                                               MODEL_PREPROCESSOR_CONFIG_FILE,
                                               MODEL_WEIGHTS_DIR)

import torch
from huggingface_hub import hf_hub_download
from loguru import logger
from transformers import AutoModel, AutoImageProcessor
import os


def download_model():
    if not MODEL_WEIGHTS_PATH.exists():
        logger.info(f'[*] {MODEL_WEIGHTS_PATH} not found! Downloading...')
        try:

            hf_hub_download(repo_id=MODEL_WEIGHTS_REPO,
                            filename=MODEL_WEIGHTS_FILE,
                            local_dir=str(MODEL_WEIGHTS_DIR))
            logger.success(f'[+] {MODEL_WEIGHTS_FILE} successfully downloaded')

            hf_hub_download(repo_id=MODEL_WEIGHTS_REPO,
                            filename=MODEL_WEIGHTS_CONFIG_FILE,
                            local_dir=str(MODEL_WEIGHTS_DIR))
            logger.success(f'[+] {MODEL_WEIGHTS_CONFIG_FILE} successfully downloaded')

            hf_hub_download(repo_id=MODEL_WEIGHTS_REPO,
                            filename=MODEL_PREPROCESSOR_CONFIG_FILE,
                            local_dir=str(MODEL_WEIGHTS_DIR))
            logger.success(f'[+] {MODEL_PREPROCESSOR_CONFIG_FILE} successfully downloaded')

        except Exception as e:
            logger.error(f'Unable to download model: {e}')
        logger.info(f"{os.listdir(MODEL_WEIGHTS_DIR)}")


def load_model():
    try:
        download_model()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"[*] Using device: {device}")

        processor = AutoImageProcessor.from_pretrained(str(MODEL_WEIGHTS_DIR))
        vision_model = AutoModel.from_pretrained(str(MODEL_WEIGHTS_DIR), trust_remote_code=True)

        logger.success("[+] Model loaded successfully")

    except Exception as e:
        logger.error(f"Unable to load model: {e}")

    return processor, vision_model


processor, vision_model = load_model()


def get_model():
    return vision_model


def get_processor():
    return processor
