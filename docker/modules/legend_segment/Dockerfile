FROM docker.uncharted.software/segmentation:latest

# INCLUDEX perms.txt

COPY . /ta1/repos/uncharted-ta1/

WORKDIR /ta1/repos/uncharted-ta1
ENV PYTHONPATH=/ta1/repos/uncharted-ta1:$PYTHONPATH

CMD []
ENTRYPOINT [ \
    "python3", "-W", "ignore", "pipelines/segmentation/run_pipeline.py" \
    ]
