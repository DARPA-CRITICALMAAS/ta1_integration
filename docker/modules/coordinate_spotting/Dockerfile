FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# Prevent interactive dialogs during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Update the package list and install libglib2.0-0
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    sudo \ 
    git \
    libgl1-mesa-glx  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y \
# #     ffmpeg \
# #     libsm6 \
# #     libxext6  \
#     sudo \ 
#     git \
#     libgl1-mesa-glx \
#     # libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install \
    Pillow==9.4.0 \
    pandas==1.4.3 \
    pyyaml \
    numpy==1.23 \
    opencv-python \
    Polygon3 \
    shapely==1.8.2 \
    geojson==2.5.0 \
    setuptools==59.5.0 \
    numba \
    scikit-image

RUN pip install 'git+https://github.com/facebookresearch/detectron2.git@v0.6'

RUN apt-get update && apt-get install sudo

# INCLUDEX perms.txt

USER root
RUN adduser cmaas sudo
RUN echo "cmaas ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
USER cmaas

# COPY ./usc-umn-inferlink-ta1 /ta1/repos/usc-umn-inferlink-ta1
# COPY ./AdelaiDet /ta1/repos/AdelaiDet

# RUN cp \
#       /ta1/repos/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/run_text_spotting.py \
#       /home/mapkurator-system/ \
#     && cp \
#       /ta1/repos/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/m3_image_geojson/stitch_output.py \
#       /home/mapkurator-system/m3_image_geojson/stitch_output.py

COPY ./ta1_integration/docker/modules/text_spotting/runme.sh \
    /ta1/text_spotting_runme.sh

CMD []
ENTRYPOINT [ \
     "/ta1/text_spotting_runme.sh" \
    ]