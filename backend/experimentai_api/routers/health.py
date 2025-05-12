from fastapi import APIRouter

health_router = APIRouter()


@health_router.get('/live', summary="Is the API live?")
def live():
    return 'LIVE'


@health_router.get('/ready', summary="Is the API ready?")
def ready():
    return 'READY'
