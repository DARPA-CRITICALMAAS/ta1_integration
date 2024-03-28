#!/bin/bash

python -c "import torch; print(f'\n\n\n!! {torch.cuda.is_available()} **\n\n\n')"

pushd /ta1/repos/Deformable-DETR/models/ops
sudo python setup.py build install
popd

python /ta1/repos/usc-umn-inferlink-ta1/line/run_line_extraction.py $@
