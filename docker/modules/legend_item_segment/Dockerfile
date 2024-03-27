FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN conda install -y -n base     scipy
RUN conda install -y -n base     matplotlib
RUN conda install -y -n base     numpy
RUN conda install -y -n base     pandas
RUN conda install -y -n base     geopandas
RUN conda install -y -n base     shapely
RUN conda install -y -n base     conda-forge::gdal
RUN conda install -y -n base     fastai::opencv-python-headless
RUN conda install -y -n base pyproj

RUN apt update && apt-get install -y \
    libtiff-dev \
    tesseract-ocr \
    libtesseract-dev \
    libvips-dev

RUN pip --no-input install \
    pytesseract \
    openai \
    pyvips \
    wandb \
    gdown \
    ipywidgets \
    rasterio

# INCLUDEX perms.txt

COPY ./usc-umn-inferlink-ta1/ /ta1/repos/usc-umn-inferlink-ta1/
COPY ./ta1_integration/docker/modules/legend_item_segment/runme.sh \
    /ta1/legend_item_segment_runme.sh

ENV TESSERACT_EXE=/usr/bin/tesseract

CMD []
ENTRYPOINT [ \
    "/ta1/legend_item_segment_runme.sh" \
    ]
