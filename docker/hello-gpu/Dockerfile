# docker build -f Dockerfile -t hello-gpu $REPO_ROOT
# docker run --gpus=all  hello-gpu

FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

RUN pip install nvidia-ml-py3

COPY ./ta1_integration /ta1/dev/ta1_integration

WORKDIR /ta1/dev/ta1_integration
ENV PYTHONPATH=/ta1/dev/ta1_integration

CMD []
ENTRYPOINT ["python", "/ta1/dev/ta1_integration/mip/apps/perf_stress.py"]
