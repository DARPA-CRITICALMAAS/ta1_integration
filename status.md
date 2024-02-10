# SYSTEM

**Now**

* complete polygon extract (#59) - UNDERWAY
* review Top Ten -- add don't write current dir
* 
* complete point extract (#45)
* complete line extract (#36)
* complete geopackage
* geopackage post-run verify
* line extract post-run verify (#30)
* point extract post-run verify (#57)
* polygon extract post-run verify (#31)
* generate perf data for WY_CO_Peach
* generate perf data for AK_Dillingham
* generate perf data for WY_CO_EatonRes
* mail to Yao-Yi: 30 min presentation, 15 min with each module owner 
* ec2 cost chart
* printouts
* update overview slides: perf (10), issues (11)

**This Week**

* coalesce dockerfile requirements
* switch to ansible
* make S3 inputs bucket public/read
* GPU perf (#64)
* host-vs-container perf
* code docs (#53)
* validate outputs against schemas (#73)


# MODULES

* wrapper script that uses just three required switches (--output-dir, --input--dir,
    --temp-dir), following the MIP directory conventions

* module input files may ONLY be:
    * the map TIF
    * static model/config/etc files in the repo or in the special S3 bucket
    * dynamic outputs from other modules
    * _NOT: files from "outside" of the system (e.g. "competition format")_

* module output files may ONLY be:
    * the output dir
    * the temp dir

* also:
    * never assume CWD (".") is accessible
    * never write to the repo
    * never download from the web (unless well-known external)

* work with me on proper requirements lists
    * include all of them
    * pin to latest versions


# LEGEND_SEGMENT (Uncharted)

* GPU (now or later)?
* package requirements


# LEGEND_ITEM_SEGMENT (Fandel)

* GPU (now or later)?
* package requirements
* downloads from internet? (#62)


# LEGEND_ITEM_DESCRIPTION (Weiwei)

* GPU (now or later)?
* package requirements
* --symbol_json_dir uses files from $INPUT_DIR (#55)


# MAP_CROP (Weiwei)

* GPU (now or later)?
* package requirements
* 


# TEXT_SPOTTING (Weiwei/Zekun)

* GPU (now or later)?
* package requirements
* 


# LINE_EXTRACT (Weiwei)

* GPU (now or later)?
* package requirements
* 


# POLYGON_EXTRACT (Fandel)

* GPU (now or later)?
* package requirements
* downloads from internet?
* 


# POINT_EXTRACT (Leeje)

* GPU (now or later)?
* package requirements
* 


# GEOREFERENCE (Weiwei)

* GPU (now or later)?
* package requirements
* 


# GEOPACKAGE (Weiwei)
 
* GPU (now or later)?
* package requirements
* 
