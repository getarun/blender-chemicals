Surface Science Physics in Blender
====================
This is an approach to model molecules at surfaces with correct dimensions and put them on a desired surface (fcc yet). Creation of hexagonal 2D-layers structured like graphene and h-BN is possible, too.
![](http://getarun.lima-city.de/blender-chemicals/render-output-3/Full-view-TOP.png)

Usage
-----
In order to locally convert files to the required format, you will need the
[Open Babel](http://openbabel.org/wiki/Main_Page) library and Python bindings
for chemical file format parsing, which is best installed from source.
For more, read through the [Open Babel installation instructions](http://openbabel.org/docs/dev/Installation/install.html).

For all those lucky unix users:

```
sudo apt-get install build-essential python-dev libpython-dev 
sudo apt-get install swig libcairo2-dev libxml2-dev zlib1g-dev libeigen3-dev libboost-dev libboost-python-dev
# sudo apt-get install git
git clone https://github.com/openbabel/openbabel
mkdir build && cd build
# sudo apt-get install cmake
cmake ../openbabel -DPYTHON_BINDINGS=ON
make && make install

sudo apt-get install blender
```
Compilation doesn't always perform like a charm, so if this fails without hope of success, look for some online-En-/Decoder.

Once you compiled and installed the format-framework, you can convert files to Javascript Object Notation with something like

```
python format_converter *data* *in_format* json > molecule.json
```

*format* is any format in [this list](https://openbabel.org/docs/dev/FileFormats/Overview.html#file-formats),
and *data* is either a string or a file containing the data specified by *format*.
From here, use `blender -P molecule_to_blender.py` to load the molecule.

Literature:
====================
[compile instructions](http://openbabel.org/docs/dev/Installation/install.html#compiling-open-babel)

[blenders python API reference](http://www.blender.org/api/blender_python_api_2_76_2/)

[blenders python extensions](http://wiki.blender.org/index.php/Extensions:2.6/Py)

[atomic data](http://www.periodictable.com/Elements/029/data.html)

[Compiling with Windows Toolchain](http://openbabel.org/wiki/Category:Installation) is a pain in the ass, but described here.
