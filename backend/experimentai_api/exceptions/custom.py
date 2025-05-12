from fastapi import HTTPException, status


class APIError(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = 'OPERATION ERROR'
        super().__init__(status_code, detail)


class RequestError(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = 'INVALID BASE64 PAYLOAD'
        super().__init__(status_code, detail)


class ModelError(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = 'UNABLE TO INSTANTIATE DOCUMENT LAYOUT PARSER MODEL'
        super().__init__(status_code, detail)


class ParserError(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = 'UNABLE TO PARSE DOCUMENT'
        super().__init__(status_code, detail)


class CUDAError(HTTPException):
    def __init__(self) -> None:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = 'CUDA UNAVAILABLE'
        super().__init__(status_code, detail)
