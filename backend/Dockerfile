FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu20.04


ARG versao=1.0.0

WORKDIR /app

ARG PROJECT_NAME=experimentai_api
ARG PROJECT_PATH=/app/${PROJECT_NAME}

# Define environment variables
ENV VERSION=${versao}



RUN apt-get -y update
RUN apt-get -y --no-install-recommends install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update
# Set python3 and pip3 to use the new version (Python 3.11)
RUN apt-get install -y \
    python3.11 \
    python3.11-distutils \
    python3.11-venv
RUN python3.11 -m ensurepip --upgrade
RUN ln -s /usr/local/bin/pip3.11 /usr/bin/pip3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.11 1
# Install OpenCV-Python dependencies
RUN apt-get -y --no-install-recommends install ffmpeg
RUN apt-get -y --no-install-recommends install libsm6
RUN apt-get -y --no-install-recommends install libxext6
# Clear the retrieved package files left in cache
RUN apt-get clean
# Remove package lists
RUN rm -rf /var/lib/apt/lists/*

COPY README.md CHANGELOG.md setup.py .
COPY ${PROJECT_NAME}/__init__.py ${PROJECT_PATH}/__init__.py
RUN pip install --no-cache-dir -e .
COPY ${PROJECT_NAME} ${PROJECT_PATH}


# Expose port 8000 to communicate with outside resources
EXPOSE 8000

CMD ["uvicorn", "experimentai_api.main:app", "--host", "0.0.0.0", "--port", "8000"]