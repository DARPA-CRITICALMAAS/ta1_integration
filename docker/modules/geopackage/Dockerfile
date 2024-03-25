FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN \
    conda install -y -n base pandas \
    && conda install -y -n base geopandas \
    && conda install -y -n base conda-forge::gdal

RUN pip install --no-input \
    criticalmaas.ta1-geopackage \
    pytest \
    rasterio

# INCLUDEX perms.txt

COPY . /ta1/dev/usc-umn-inferlink-ta1/

CMD []
ENTRYPOINT [ \
    "python", "/ta1/dev/usc-umn-inferlink-ta1/system/gpkg_generation/src/run_gpkg_writer.py" \
]
