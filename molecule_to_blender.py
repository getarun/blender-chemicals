#!/usr/bin/env python
"""
Loads a json molecule and draws atoms in Blender.

Blender scripts are weird. Either run this inside of Blender or in a shell with
    blender foo.blend -P molecule_to_blender.py

The script expects an input file named "molecule.json" and should be in the
same directory as "atoms.json"

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""

import bpy
from math import acos
from mathutils import Vector
import json
import os

# Get path of this file (useful when this script is imported)
PATH = os.path.dirname(os.path.realpath(__file__))

# Atomic radii from wikipedia, scaled to Blender radii (C = 0.4 units)
# http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page)
# Atomic colors from cpk
# http://jmol.sourceforge.net/jscolors/
with open(os.path.join(PATH, "atoms.json")) as in_file:
    atom_data = json.load(in_file)


def draw_molecule(substrate, center=(0, 0, 0), max_molecule_size=5):
    """Draw a molecule to blender. Uses loaded json molecule data."""
    scale = 0.5
    # Get scale factor - only scales large molecules down
    max_coord = 1E-6
    for atom in substrate["atoms"]:
        max_coord = max(max_coord, *[abs(a) for a in atom["location"]])
    scale = min(max_molecule_size / max_coord, 1)

    # Scale location coordinates and add specified center
    for atom in substrate["atoms"]:
        atom["location"] = [c + x * scale for c, x in zip(center,atom["location"])]

    # Keep references to all atoms and bonds
    shapes = []

    # Add atom primitive
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object

    # Draw atoms
    for atom in substrate["atoms"]:

        # If element is not in dictionary, use undefined values
        if atom["element"] not in atom_data:
            atom["element"] = "undefined"

        # If material for atom type has not yet been defined, do so
        if atom["element"] not in bpy.data.materials:
            key = atom["element"]
            bpy.data.materials.new(name=key)
            bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
            bpy.data.materials[key].specular_intensity = 0.2

        # Copy mesh primitive and edit to make atom
        atom_sphere = sphere.copy()
        atom_sphere.data = sphere.data.copy()
        atom_sphere.location = atom["location"]
        atom_sphere.dimensions = [atom_data[atom["element"]]["radius"]* 2 * scale] * 3
        atom_sphere.active_material = bpy.data.materials[atom["element"]]
        bpy.context.scene.objects.link(atom_sphere)
        shapes.append(atom_sphere)


    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
   
    # If the starting cube is there, remove it
    if "Cube" in bpy.data.objects.keys():
        bpy.data.objects.get("Cube").select = True
    bpy.ops.object.delete()

    # Smooth and join molecule shapes
    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]
    bpy.ops.object.shade_smooth()
    bpy.ops.object.join()

    # Center object origin to geometry
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

    # Refresh scene
    bpy.context.scene.update()

# Runs the method
if __name__ == "__main__":
    with open("substrate.json") as molecule_file:
        substrate = json.load(molecule_file)
    draw_molecule(substrate)
