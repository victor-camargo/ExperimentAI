from pydantic import BaseModel
from typing import List

EXAMPLE_IMAGE_B64 = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1"
                     "BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdj"
                     "YAAAAAIAAeIhvDMAAAAASUVORK5CYII=")


class RequestImageBase64(BaseModel):

    image_b64: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'image_b64': EXAMPLE_IMAGE_B64
                }
            ]
        }
    }


class ScorePayload(BaseModel):
    id: str
    score: float
    payload: dict

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': '1234567890',
                    'score': 0.99,
                    'payload': {
                            'equipamento': 'rampa',
                            'descricao': 'Rampa de inclinação ajustável para experimentos de dinâmica. Fabricada em alumínio, com superfície antiderrapante.',
                            'instrucoes': 'Para ajustar a inclinação, solte os parafusos de fixação e mova a rampa para a posição desejada. Aperte os parafusos novamente para garantir a estabilidade.',
                            'exemplo': 'Exemplo de uso: Colocar uma esfera na parte superior da rampa e medir o tempo que leva para chegar ao fundo. Usar um cronômetro para registrar o tempo.',
                            'observacoes': 'Certifique-se de que a rampa esteja nivelada antes de iniciar os experimentos. Evite colocar peso excessivo na rampa para não danificá-la.',
                            'image_path': 'Labpics\\rampa\\20250331_083038.jpg'
                    }
                }
            ]
        }
    }


class ResponseVSS(BaseModel):

    similarity_results: List[ScorePayload]

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'similarity_results': [ScorePayload.model_config['json_schema_extra']['examples'][0],
                                           ScorePayload.model_config['json_schema_extra']['examples'][0]]
                }
            ]
        }
    }