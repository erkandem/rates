#!/bin/bash
which python
python -V
pip -V
pip install --upgrade virtualenv
pip install -r ./requirements/builddeps.txt
