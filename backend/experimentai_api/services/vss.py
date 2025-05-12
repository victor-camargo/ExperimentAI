from typing import List

from loguru import logger

import torch
import torch.nn.functional as F

from experimentai_api.exceptions.custom import (APIError,
                                                CUDAError,
                                                ParserError,
                                                RequestError)
from experimentai_api.utils.process import b64_to_pil
from experimentai_api.configs.settings import (QDRANT_URL,
                                               QDRANT_API_KEY,
                                               QDRANT_COLLECTION,
                                               QDRANT_SEARCH_LIMIT)

from transformers import AutoModel, AutoImageProcessor
import requests


class VectorSimilaritySearchService:

    def vss(self,
            image_b64: str,
            processor: AutoImageProcessor,
            model: AutoModel):
        """Receives an image and reads text on them."""
        try:
            image_pil = b64_to_pil(image_b64)
            embeddings = self._generate_embeddings(processor,
                                                   model,
                                                   image_pil)
            response = self._vector_db_search(embeddings)
        except ValueError:
            raise RequestError
        except TypeError:
            raise ParserError
        except CUDAError:
            raise
        except Exception as e:
            logger.error(f'[-] Unexpected error: {e}')
            raise APIError
        return response

    def _generate_embeddings(self,
                             processor,
                             model,
                             image_pil):
        """Private method. Receives an image tensor and uses the model to generate embeddings"""
        try:
            inputs = processor(images=image_pil, return_tensors="pt")
            with torch.no_grad():
                image_features = model(**inputs).last_hidden_state
                embeddings = F.normalize(image_features[:, 0], p=2, dim=1)
                embeddings = embeddings.reshape(-1).cpu().numpy()
        except TypeError as e:
            logger.error(f'[-] TypeError: {e}')
            raise
        return embeddings

    def _vector_db_search(self,
                          embeddings: List[float],):

        """Private method. Receives an image embedding and
        searches for similar images in the database"""

        try:
            response = requests.post(
                f'{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points/query',
                headers={
                    'Content-Type': 'application/json',
                    'api-key': QDRANT_API_KEY
                },
                json={
                    "query": embeddings.tolist(),
                    "limit": QDRANT_SEARCH_LIMIT,
                    "with_payload": True
                }
            )

            if response.status_code != 200:
                logger.error(f'[-] Error: {response.status_code}')
                return None

            data = response.json()['result']['points']

            for k, point in enumerate(data):
                data[k]['score'] = round((point['score'] + 1)*50, 2) # Normalize COS_SIM

        except requests.exceptions.RequestException as e:
            logger.error(f'[-] RequestException: {e}')
            raise APIError
        except Exception as e:
            logger.error(f'[-] Unexpected error: {e}')
            raise APIError
        return data
