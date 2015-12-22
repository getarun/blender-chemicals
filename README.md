Chemicals in Blender
====================
Full credit to http://patrick-fuller.com/molecules-from-smiles-molfiles-in-blender/

useful: http://openbabel.org/docs/dev/Installation/install.html#compiling-open-babel

useful: http://blender.stackexchange.com/questions/9200/make-object-a-a-parent-of-object-b-via-python

useful: https://openbabel.org/docs/dev/FileFormats/Overview.html#file-formats

useful: http://www.blender.org/api/blender_python_api_2_76_2/

useful: http://wiki.blender.org/index.php/Extensions:2.6/Py 

atomic data: http://www.periodictable.com/Elements/029/data.html


requires packages in ubuntu: gcc4

Draws chemicals in Blender using common input formats (smiles, molfiles, cif files,
etc.). For details, read my [blog post](http://www.patrick-fuller.com/molecules-from-smiles-molfiles-in-blender/).

Usage
-----

In order to locally convert files to the required format, you will need the
[Open Babel](http://openbabel.org/wiki/Main_Page) library and Python bindings
for chemical file format parsing, which is best installed from source.
For more, read through the [Open Babel installation instructions](http://openbabel.org/docs/dev/Installation/install.html).

```
sudo apt-get install build-essential python-dev libpython-dev libcairo2-dev libxml2-dev zlib1g-dev libeigen2-dev

git clone https://github.com/openbabel/openbabel
mkdir build && cd build
cmake ../openbabel -DPYTHON_BINDINGS=ON
make && make install

sudo apt-get install blender
```

From here, you can convert files to Javascript Object Notation with something like

```
python format_converter *data* *in_format* json > molecule.json
```

*format* is any format in [this list](http://openbabel.org/docs/2.3.0/FileFormats/Overview.html),
and *data* is either a string or a file containing the data specified by *format*.
From here, use `blender -P molecule_to_blender.py` to load the molecule.

The shell script is a light wrapper around these two commands. For example,

```bash
sh draw_molecule.sh "CC(C)(C)C1=CC2(C=C(C(C)(C)C)C1=O)CC2(c1ccccc1)c1ccccc1" smi
```

will convert the input data (string or file path) and load into Blender.

Compiling with Windows Toolchain is a pain in the ass, but described here:

http://openbabel.org/wiki/Category:Installation
