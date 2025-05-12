import base64
import binascii
import io
from io import BytesIO

from loguru import logger
from PIL import Image, UnidentifiedImageError


def b64_to_pil(image_b64: str) -> Image.Image:
    """Receives a valid base64-encoded image and converts it to a PIL Image object"""
    try:
        decoded = base64.b64decode(image_b64)
        buf = io.BytesIO(decoded)
        image_pil = Image.open(buf)
        if image_pil.mode != 'RGB':
            image_pil = image_pil.convert('RGB')
        return image_pil
    except binascii.Error as e:
        logger.error(f'[-] Error decoding base64 string: {e}')
        raise ValueError('INVALID BASE64 STRING')
    except UnidentifiedImageError as e:
        logger.error(f'[-] Error opening base64 string as PIL Image: {e}')
        raise ValueError('INVALID BASE64 STRING')


def pil_to_b64(image_pil: Image.Image) -> str:
    """Receives a valid PIL Image object and converts it to a base64-encoded image"""
    try:
        buf = BytesIO()
        image_pil.save(buf, format="PNG")
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        return img_str
    except Exception as e:
        logger.error(f"[-] Error converting Pillow Image to Base64 string: {e}")
        raise
