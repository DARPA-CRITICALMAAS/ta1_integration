#!/bin/bash
set -e
set -x

python -c "import torch; print(f'\n\n\n..... {torch.cuda.is_available()} **\n\n\n')"

#cd /ta1/dev

#git clone https://github.com/fundamentalvision/Deformable-DETR.git

cd /ta1/dev/Deformable-DETR/models/ops

sh ./make.sh

#python setup.py build install
