# syntax=docker/dockerfile:experimental
FROM tensorflow/tensorflow:latest-gpu-jupyter
WORKDIR /tf
COPY . .
RUN python -m pip install -r requirements.txt
