from fastapi import FastAPI
import uvicorn
from loguru import logger
from experimentai_api.routers import health_router, start_router, vss_router
from experimentai_api import __version__
from experimentai_api.utils.models import get_model, get_processor
from experimentai_api.configs.settings import MODEL_INPUT_DIM, N_ITER_STARTUP_INFERENCE
from experimentai_api.configs.loguru import set_logger_configs


import numpy as np
import torch

from PIL import Image

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    # Add other allowed origins here
]




@asynccontextmanager
async def lifespan(app: FastAPI):
    """This contains logic that is executed before the application starts up.
    Any logic after the `yield` is executed on application shutdown.

    This is done to load the entire model on memory before receiving any requests.
    """
    logger.info('[*] Performing startup inferences to fully load NougatOCR model...')
    processor = get_processor()
    model = get_model()
    input_tensor = np.zeros((MODEL_INPUT_DIM, MODEL_INPUT_DIM, 3), np.uint8)
    image_pil = Image.fromarray(input_tensor)

    for _ in range(N_ITER_STARTUP_INFERENCE):
        inputs = processor(images=image_pil, return_tensors="pt")
        with torch.no_grad():
            image_features = model(**inputs)
        del image_features
        torch.cuda.empty_cache()  # free up memory
    logger.info('[*] Startup inferences executed. Model load complete!')
    yield


def create_app():
    set_logger_configs()

    app = FastAPI(
        title='ExperimentAI API',
        description=(
            'This API uses a machine learning model to search most similar equipments'),
        openapi_url="/api/experimentai/openapi.json",
        docs_url="/api/experimentai/docs",
        redoc_url="/api/experimentai/redoc",
        version=__version__,
        lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix="/api/experimentai/health", tags=['Health'])
    app.include_router(start_router, prefix= '/api/experimentai', tags=['Start'])
    app.include_router(vss_router, prefix= '/api/experimentai', tags=['Vector Similarity Search'])

    logger.success("[+] APPLICATION CREATED AND READY TO USE.")
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="debug", port=8000)
