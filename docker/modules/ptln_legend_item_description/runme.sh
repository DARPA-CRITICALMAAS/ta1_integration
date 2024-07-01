#!/bin/bash

python -c "import torch; print(f'\n\n\n!! {torch.cuda.is_available()} **\n\n\n')"

# pushd /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3
# echo "Current directory is:"
# pwd
# sudo pip install -e .
# # python setup.py build develop
# # python -c "import layoutlmft; print(layoutlmft.__file__)"
# popd

python /ta1/repos/usc-umn-inferlink-ta1/segmentation/layoutlmv3/run_ptln_legend_item_description.py $@