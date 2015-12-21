# Generate molecule json
# $1 - either a string or a file correlated to the type specified in $2
# $2 - any input format supported by openbabel
# python format_converter.py $1 $2 json > molecule.json

#hardcoded for testing
#python format_converter.py 2mol.hin hin json > molecule.json
blender molecule.blend -P molecule_to_blender.py
