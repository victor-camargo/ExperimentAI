import time

from fastapi import APIRouter, Depends
from loguru import logger

from experimentai_api.schemas.vss import RequestImageBase64, ResponseVSS
from experimentai_api.utils.models import get_model, get_processor
from experimentai_api.services.vss import VectorSimilaritySearchService

vss_router = APIRouter()


@vss_router.post('/vss',
                 summary=('Vector Similarity Search on images'),
                 response_model=ResponseVSS)
async def predict(request: RequestImageBase64,
                  processor=Depends(get_processor),
                  model=Depends(get_model)):
    start_time = time.time()
    logger.info(f'[*] Received image for VSS: {request.image_b64[:20]}')
    vss_service = VectorSimilaritySearchService()
    vss_results = vss_service.vss(request.image_b64,
                                  processor,
                                  model)
    response = ResponseVSS(similarity_results=vss_results)

    logger.info(f'[*] Sucessful Retrieval for image: {request.image_b64[:20]}')

    latency = round(time.time() - start_time, 10)
    logger.log('LATENCY', f'[*] Latency: {latency} s')
    return response
