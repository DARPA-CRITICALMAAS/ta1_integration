FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN \
    conda install -y -n base scipy \
    && conda install -y -n base matplotlib \
    && conda install -y -n base numpy \
    && conda install -y -n base pandas \
    && conda install -y -n base geopandas \
    && conda install -y -n base shapely \
    && conda install -y -n base conda-forge::gdal \
    && conda install -y -n base fastai::opencv-python-headless

RUN apt-get install -y \
    libtiff-dev \
    tesseract-ocr \
    libtesseract-dev

RUN pip --no-input install \
    pytesseract \
    openai

ARG openai_api_key
ENV OPENAI_API_KEY=$openai_api_key

# INCLUDEX perms.txt

COPY . /ta1/repos/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/repos/usc-umn-inferlink-ta1/segmentation/legend_item_description_segment/src/gpt4_main.py" \
    ]
