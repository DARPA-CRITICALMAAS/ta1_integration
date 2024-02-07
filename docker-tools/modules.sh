#!/bin/bash
set -e

export LEGEND_SEGMENT=dockers/2_legend_segment
export LEGEND_ITEM_SEGMENT=dockers/3_legend_item_segment
export LEGEND_ITEM_DESCRIPTION=dockers/4_legend_item_description
export MAP_CROP=dockers/5_map_crop
export TEXT_SPOTTING=dockers/6_text_spotting
export LINE_EXTRACT=dockers/7_line_extract
export POLYGON_EXTRACT=dockers/8_polygon_extract
export POINT_EXTRACT=dockers/9_point_extract
export GEOREFERENCE=dockers/10_georeference

export MODULE_DIRS=" \
    $LEGEND_SEGMENT \
    $LEGEND_ITEM_SEGMENT \
    $LEGEND_ITEM_DESCRIPTION \
    $MAP_CROP \
    $TEXT_SPOTTING \
    $LINE_EXTRACT \
    $POLYGON_EXTRACT \
    $POINT_EXTRACT \
    $GEOREFERENCE \
"

export MODULE_IMAGES=" \
    inferlink/ta1_legend_segment \
    inferlink/ta1_legend_item_segment \
    inferlink/ta1_legend_item_description \
    inferlink/ta1_map_crop \
    inferlink/ta1_text_spotting \
    inferlink/ta1_line_extract \
    inferlink/ta1_polygon_extract \
    inferlink/ta1_point_extract \
    inferlink/ta1_georeference \
"
