# Start from the official PyTorch image as the base image
FROM pytorch/pytorch:1.8.1-cuda10.2-cudnn7-devel

# Remove Conda (python3.7) installation
RUN /opt/conda/bin/conda clean -tipsy && \
    rm -rf /opt/conda


RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# Install Python 3.8
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.8 python3.8-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the Python 3.8 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN python -m pip install --upgrade pip

# Install pip for the new Python version
RUN apt-get update && apt-get install -y python3-pip \
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install some tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        ccache \
        cmake \
        curl \
        git \
        libjpeg-dev \
        libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# Update the package list and install GCC
RUN apt-get update && \
    apt-get install -y gcc && \
    # Clean up the apt cache to reduce the image size
    rm -rf /var/lib/apt/lists/*

# Install pytroch
RUN pip install torch==1.8.1+cu102 torchvision==0.9.1+cu102 -f https://download.pytorch.org/whl/torch_stable.html

# Install GDAL dependencies
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install GDAL Python bindings
RUN pip install GDAL==$(gdal-config --version)

RUN pip install \
    opencv-python \
    PyYAML \
    shapely==1.8.5.post1 \
    monai==0.7.0 \
    tqdm \
    scipy \
    imageio \
    pyvista \
    geopandas \
    ignite==1.1.0 \
    pytorch-ignite==0.4.9

# Install libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set env vars for cuda
ENV NVCC /usr/local/cuda/bin/nvcc
ENV CUDA_HOME /usr/local/cuda
ENV PATH /usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:${LD_LIBRARY_PATH}
ENV NVIDIA-SMI /usr/bin/nvidia-smi

RUN git clone https://github.com/fundamentalvision/Deformable-DETR.git /ta1/dev/Deformable-DETR

RUN apt-get update && apt-get install sudo

# INCLUDEX perms.txt

USER root
RUN adduser cmaas sudo
RUN echo "cmaas ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
USER cmaas

COPY ./usc-umn-inferlink-ta1/ /ta1/dev/usc-umn-inferlink-ta1/


COPY ./ta1_integration/docker/modules/line_extract/runme.sh \
    /home/cmaas/line_extract_runme.sh

CMD []
ENTRYPOINT [ \
    "python", "-m", "ilperf", "-d", "5", "-o", "/ta1/output/line_extract/ilperf_docker.json", "--exec", \
    "/home/cmaas/line_extract_runme.sh" \
    ]
