FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

# Prevent interactive dialogs during package installation
# ARG DEBIAN_FRONTEND=noninteractive
# Set MKL threading layer to GNU (compatible with libgomp)
ENV MKL_THREADING_LAYER=GNU
# Update the package list and install libglib2.0-0
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    sudo \
    libgl1-mesa-glx  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# # Install Rust
# RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"
# RUN rustc --version

# Install system dependencies for Python packages and Rust
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    cargo \
    tesseract-ocr \
    tesseract-ocr-eng

# # Clone the tokenizers repository
# RUN git clone https://github.com/huggingface/tokenizers.git

# WORKDIR tokenizers/bindings/python
# # Build the wheel manually
# RUN python setup.py bdist_wheel
# # Install the wheel
# RUN pip install dist/*.whl
# # Clean up unnecessary files
# RUN rm -rf tokenizers

RUN pip install setuptools==69.5.1

RUN pip install \
    # tokenizers \
    datasets==1.15.1 \
    transformers==4.17.0 \
    seqeval==1.2.2 \
    deepspeed==0.5.7 \
    tensorboard==2.7.0 \
    seqeval==1.2.2 \
    # sentencepiece \
    timm==0.4.12 \
    Pillow==9.1.0 \
    einops \
    textdistance \
    shapely \
    pytesseract

RUN pip install 'git+https://github.com/facebookresearch/detectron2.git@v0.6'

RUN apt-get update && apt-get install sudo

COPY ./usc-umn-inferlink-ta1/segmentation/layoutlmv3 /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3
RUN chmod -R 777 /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3

# INCLUDEX perms.txt
USER root
RUN adduser cmaas sudo
RUN echo "cmaas ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN chown -R cmaas /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3
USER cmaas

WORKDIR /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3
RUN pip install -e . --verbose

COPY ./ta1_integration/docker/modules/ptln_legend_item_description/runme.sh \
    /ta1/ptln_legend_item_description_runme.sh

CMD []
ENTRYPOINT [ \
     "/ta1/ptln_legend_item_description_runme.sh" \
    ]