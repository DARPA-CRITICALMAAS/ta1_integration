FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN conda install -y -n base \
    pandas==2.0.3 \
    geopandas==0.13.2 \
    conda-forge::gdal==3.6.2

RUN pip install criticalmaas.ta1-geopackage
RUN pip install pytest

#RUN apt-get install -y libtiff-dev

#    scipy \
#    matplotlib \
#    numpy \
#    shapely==2.0.1 \
#    fastai::opencv-python-headless


# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", \
    "/ta1/dev/usc-umn-inferlink-ta1/system/gpkg_generation/run_gpkg_writer.py" \
]
