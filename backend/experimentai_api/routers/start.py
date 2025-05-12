from fastapi import APIRouter

start_router = APIRouter()


@start_router.get('/',
                  summary="Welcome to the ExperimentAI API.")
def start():
    return ("Welcome to the ExperimentAI API."
            "Access the API's documentation at /docs.")
