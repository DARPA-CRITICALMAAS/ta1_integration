FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN conda install -y -n base \
    scipy \
    matplotlib \
    numpy \
    pandas==2.0.3 \
    geopandas==0.13.2 \
    shapely==2.0.1 \
    conda-forge::gdal==3.6.2 \
    fastai::opencv-python-headless

RUN apt update \
    && apt-get install -y libtiff-dev tesseract-ocr libtesseract-dev libvips-dev \
    && pip --no-input install pytesseract openai pyvips wandb gdown \
    && conda install -y -n base rasterio pyproj

RUN pip --no-input install ipywidgets

# INCLUDEX perms.txt

COPY ./usc-umn-inferlink-ta1/ /ta1/dev/usc-umn-inferlink-ta1/
COPY ./ta1_integration/docker/modules/legend_item_segment/runme.sh \
    /home/cmaas/legend_item_segment_runme.sh

ENV TESSERACT_EXE=/usr/bin/tesseract

CMD []
ENTRYPOINT [ \
    "/home/cmaas/legend_item_segment_runme.sh" \
    ]
