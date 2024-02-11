FROM knowledgecomputing/mapkurator_recogito_2023:latest

COPY ./usc-umn-inferlink-ta1 /ta1/dev/usc-umn-inferlink-ta1

RUN cp \
    /ta1/dev/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/run_text_spotting.py \
    /home/mapkurator-system/

RUN cp \
    /ta1/dev/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/m3_image_geojson/stitch_output.py \
    /home/mapkurator-system/m3_image_geojson/stitch_output.py

COPY ./ta1_integration/docker/modules/text_spotting/runme.sh \
    /home/cmaas/text_spotting_runme.sh
    
# INCLUDEX perms.txt

CMD []
ENTRYPOINT [ "/home/cmaas/text_spotting_runme.sh" ]
