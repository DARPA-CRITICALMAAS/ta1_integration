FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN \
    conda install -y -n base pandas \
    && conda install -y -n base geopandas \
    && conda install -y -n base conda-forge::gdal

RUN pip install --no-input \
    pytest \
    rasterio
RUN pip install git+https://github.com/DARPA-CRITICALMAAS/ta1-geopackage.git

# INCLUDEX perms.txt

COPY . /ta1/repos/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/repos/usc-umn-inferlink-ta1/system/gpkg_generation/src/run_gpkg_writer.py" \
]
