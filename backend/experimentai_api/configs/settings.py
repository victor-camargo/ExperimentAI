import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = APP_DIR.joinpath('logs')


EXPERIMENTAI_LOGS_FILE = LOGS_DIR.joinpath('experimentai.log')
EXPERIMENTAI_ERROR_LOGS_FILE = LOGS_DIR.joinpath('experimentai.error.log')


QDRANT_URL = os.environ.get('QDRANT_URL', 'http://labcc.ddns.net:8010')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY', '')
QDRANT_COLLECTION = os.environ.get('QDRANT_COLLECTION', 'ExperimentAI_dev')
QDRANT_SEARCH_LIMIT = int(os.environ.get('QDRANT_SEARCH_LIMIT', 10))

MODEL_WEIGHTS_REPO = os.environ.get('MODEL_WEIGHTS_REPO',
                                    'nomic-ai/nomic-embed-vision-v1.5')

MODEL_WEIGHTS_FILE = os.environ.get('MODEL_WEIGHTS_FILE',
                                    'model.safetensors')

MODEL_WEIGHTS_CONFIG_FILE = os.environ.get('MODEL_CONFIG_FILE',
                                           'config.json')

MODEL_PREPROCESSOR_CONFIG_FILE = os.environ.get('MODEL_PREPROCESSOR_CONFIG_FILE',
                                                'preprocessor_config.json')

MODEL_WEIGHTS_DIR = APP_DIR.joinpath('weights')

MODEL_WEIGHTS_PATH = MODEL_WEIGHTS_DIR.joinpath(MODEL_WEIGHTS_FILE)

MODEL_INPUT_DIM = int(os.environ.get('MODEL_INPUT_DIM', '1024'))
N_ITER_STARTUP_INFERENCE = int(os.environ.get('N_ITER_STARTUP_INFERENCE', 3))

Path.mkdir(LOGS_DIR, exist_ok=True)
Path.mkdir(MODEL_WEIGHTS_DIR, exist_ok=True)
