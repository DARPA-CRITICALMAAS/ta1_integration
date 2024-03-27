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

RUN apt-get install -y libtiff-dev

# INCLUDEX perms.txt

COPY . /ta1/repos/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/repos/usc-umn-inferlink-ta1/system/image_crop/map2patch.py" \
]
