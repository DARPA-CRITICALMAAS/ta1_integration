FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git
RUN conda install -y -n base fastai::opencv-python-headless
RUN pip install \
    pandas \
    transformers@git+https://github.com/zekun-li/transformers@geolm \
    segment_anything@git+https://github.com/facebookresearch/segment-anything.git \
    rank_bm25 \
    scikit-image \
    matplotlib

#RUN conda install -y -n base
#scipy scikit-image
#torch==2.1.0
#rank_bm25
#geopandas
#folium
#rasterio
#streamlit_folium
#torchvision==0.16.0

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

WORKDIR /ta1/dev/usc-umn-inferlink-ta1/georeferencing/text-based

CMD []
ENTRYPOINT ["python", "-W", "ignore", \
    "/ta1/dev/usc-umn-inferlink-ta1/georeferencing/text-based/run_georenference.py"]
