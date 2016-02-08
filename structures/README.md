========
How to create structural python script to import molecules from for example pubchem database:
========

Download the model (tested cif and sdf, pdb) and convert it using openbabel and the format_converter-script.

The tested way is to convert it to json file format and translate this to blender with a python script.

Copy one of the python script files, that are contained in the repository and simply change the last line to the correct path to your python script file

Save it somewhere and call "blender -P /where/you/saved/the/file/"

Be sure to have the "atoms.json" in the same directory where the pyton script file you call is located.

'#### All-In one:
'#!/bin/bash '  
'python ../format_converter/format_converter.py INPUTFILE.INFILETYPE INFILETYPE OUTFILETYPE > OUTPUTFILE.OUTFILETYPE '  
'# rewrite python script file to match correct path and check existence of atoms.json '  
'blender -P pythonscriptfile.py '  
