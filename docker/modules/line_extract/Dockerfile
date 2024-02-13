FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel

# INCLUDEX base.txt

RUN conda install -y -n base \
    scipy
RUN conda install -y -n base \
    matplotlib
RUN conda install -y -n base \
    numpy
RUN conda install -y -n base \
    conda-forge::gdal==3.6.2
RUN conda install -y -n base \
    pandas==2.0.3 \
    geopandas==0.13.2 \
    shapely==2.0.1
RUN conda install -y -n base \
    fastai::opencv-python-headless

RUN apt-get install -y libtiff-dev

RUN pip install monai imageio pyvista

# ... RUN pip install MultiScaleDeformableAttention ...

RUN apt-get install -y git
RUN git clone https://github.com/fundamentalvision/Deformable-DETR.git /ta1/dev/Deformable-DETR
RUN pip install pytorch-ignite

# INCLUDEX perms.txt

COPY ./usc-umn-inferlink-ta1/ /ta1/dev/usc-umn-inferlink-ta1/

#CMD []
#ENTRYPOINT ["python", "/ta1/dev/usc-umn-inferlink-ta1/line/run_line_extraction.py"]
#ENTRYPOINT ["python", "/ta1/dev/usc-umn-inferlink-ta1/integration/docker-tools/always_pass.py"]

COPY ./ta1_integration/docker/modules/line_extract/runme.sh \
    /home/cmaas/line_extract_runme.sh

ENTRYPOINT ["/home/cmaas/line_extract_runme.sh"]
