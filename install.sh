#!/bin/bash

sudo apt-get install python-dev libpython-dev 
sudo apt-get install libcairo2-dev libxml2-dev zlib1g-dev libeigen2-dev

git clone https://github.com/openbabel/openbabel
mkdir build && cd build
cmake ../openbabel -DPYTHON_BINDINGS=ON
make && sudo make install

