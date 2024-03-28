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

RUN apt-get update && apt-get install -y \
    libtiff-dev \
    libvips-dev

RUN pip --no-input install \
    scikit-image \
    Pillow==9.4.0 \
    rasterio \
    wandb \
    pyvips \
    gdown

RUN conda install -y -c conda-forge ipywidgets

# INCLUDEX perms.txt

COPY . /ta1/repos/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/repos/usc-umn-inferlink-ta1/polygon/loam_handler.py" \
    ]
