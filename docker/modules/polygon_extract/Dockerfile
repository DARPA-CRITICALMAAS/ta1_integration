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

RUN apt-get install -y libtiff-dev

RUN pip --no-input install scikit-image Pillow==9.4.0 rasterio wandb

RUN apt-get update \
    && apt-get -y install libvips-dev \
    && pip --no-input install pyvips

RUN conda install -c conda-forge ipywidgets

RUN pip --no-input install gdown

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/dev/usc-umn-inferlink-ta1/polygon/loam_handler.py" \
    ]
