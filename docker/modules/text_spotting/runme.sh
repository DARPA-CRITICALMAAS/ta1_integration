#!/bin/bash

python -c "import torch; print(f'\n\n\n!! {torch.cuda.is_available()} **\n\n\n')"

pushd /ta1/repos/AdelaiDet
sudo python setup.py build develop
popd

python /ta1/repos/usc-umn-inferlink-ta1/system/mapkurator/mapkurator-system/run_text_spotting.py $@
