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

RUN apt-get install -y libtiff-dev \
    && apt-get install -y tesseract-ocr libtesseract-dev \
    && pip --no-input install pytesseract \
    && pip --no-input install --upgrade openai

ARG openai_api_key
ENV OPENAI_API_KEY=$openai_api_key

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/dev/usc-umn-inferlink-ta1/segmentation/legend_item_description_segment/src/gpt4_main.py" \
    ]
