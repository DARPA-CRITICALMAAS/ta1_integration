FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git
RUN conda install -y -n base fastai::opencv-python-headless

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
    scikit-learn==1.3.0

RUN pip install --no-input  \
    transformers@git+https://github.com/zekun-li/transformers@geolm
RUN pip install --no-input  \
    pytesseract

RUN conda install -y -n base conda-forge::gdal==3.6.2

#RUN conda install -y -n base \
#    geopandas \
#    rasterio

RUN pip install geopandas rasterio

#    torch==2.0.1 \
# statistics                    1.0.3.5
# argparse                     1.4.0
# logging                       0.4.9.6
# collection                    0.1.6
# >> torchvision                   0.15.2
#RUN apt-get install -y libtiff-dev

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "-m", "ilperf", "-d", "5", "-o", "/ta1/output/point_extract/ilperf_docker.json", "--exec", \
    "python", "/ta1/dev/usc-umn-inferlink-ta1/point/point-symbol-pipeline/Program/run_final_text.py" \
    ]
