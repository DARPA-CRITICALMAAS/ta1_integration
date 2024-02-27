FROM docker.uncharted.software/segmentation:latest

# INCLUDEX perms.txt

COPY . /ta1/dev/uncharted-ta1/

WORKDIR /ta1/dev/uncharted-ta1
ENV PYTHONPATH=/ta1/dev/uncharted-ta1:$PYTHONPATH

CMD []
ENTRYPOINT [ \
    "python3", "-m", "ilperf", "-d", "5", "-o", "/ta1/output/legend_segment/ilperf_docker.json", "--exec", \
    "python3", "-W", "ignore", "pipelines/segmentation/run_pipeline.py" \
    ]
