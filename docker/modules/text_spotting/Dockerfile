FROM knowledgecomputing/mapkurator_recogito_2023:latest

COPY ./usc-umn-inferlink-ta1 /ta1/repos/usc-umn-inferlink-ta1

RUN cp \
      /ta1/repos/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/run_text_spotting.py \
      /home/mapkurator-system/ \
    && cp \
      /ta1/repos/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/m3_image_geojson/stitch_output.py \
      /home/mapkurator-system/m3_image_geojson/stitch_output.py

COPY ./ta1_integration/docker/modules/text_spotting/runme.sh \
    /ta1/text_spotting_runme.sh

# INCLUDEX perms.txt

CMD []
ENTRYPOINT [ \
    "/ta1/text_spotting_runme.sh" \
    ]
