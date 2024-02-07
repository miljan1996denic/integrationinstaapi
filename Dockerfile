ARG DOCKER_BASE_IMAGE_REGISTRY=docker.io/library
ARG DOCKER_BASE_IMAGE_REPOSITORY=python
ARG DOCKER_BASE_IMAGE_TAG=3.8.3-slim
FROM ${DOCKER_BASE_IMAGE_REGISTRY}/${DOCKER_BASE_IMAGE_REPOSITORY}:${DOCKER_BASE_IMAGE_TAG}
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app/
CMD ["uvicorn", "app.main:app" ,"--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive" , "3600" ]
