FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6  \
    git

RUN \
    conda install -y -n base fastai::opencv-python-headless \
    && conda install -y -n base conda-forge::gdal

RUN pip install \
    nltk==3.8.1 \
    numpy==1.24.3 \
    pandas==2.1.1 \
    matplotlib==3.8.0 \
    Pillow==9.4.0 \
    jsons==1.6.3 \
    geojson==3.1.0 \
    ultralytics==8.1.2 \
    easyocr==1.7.1 \
    kneed==0.8.5 \
    scikit-learn==1.3.0 \
    transformers@git+https://github.com/zekun-li/transformers@geolm \
    pytesseract \
    geopandas \
    rasterio

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/dev/usc-umn-inferlink-ta1/point/src/pipeline-scripts/run_point_pipe.py" \
    ]
