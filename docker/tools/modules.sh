#!/bin/bash
set -e

export LEGEND_SEGMENT=docker/legend_segment
export LEGEND_ITEM_SEGMENT=docker/legend_item_segment
export LEGEND_ITEM_DESCRIPTION=docker/legend_item_description
export MAP_CROP=docker/map_crop
export LINE_EXTRACT=docker/line_extract
export POLYGON_EXTRACT=docker/polygon_extract
export POINT_EXTRACT=docker/point_extract
export GEOREFERENCE=docker/georeference

export MODULE_DIRS=" \
    $LEGEND_SEGMENT \
    $LEGEND_ITEM_SEGMENT \
    $LEGEND_ITEM_DESCRIPTION \
    $MAP_CROP \
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
    inferlink/ta1_line_extract \
    inferlink/ta1_polygon_extract \
    inferlink/ta1_point_extract \
    inferlink/ta1_georeference \
"
