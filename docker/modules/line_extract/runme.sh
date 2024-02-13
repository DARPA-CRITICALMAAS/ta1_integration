#!/bin/bash

python -c "import torch; print(f'\n\n\n!! {torch.cuda.is_available()} **\n\n\n')"

pushd /ta1/dev/Deformable-DETR/models/ops
 python setup.py build install
popd

python /ta1/dev/usc-umn-inferlink-ta1/line/run_line_extraction.py $@
