#!/usr/bin/env python

import bpy
from math import sin,cos,sqrt
from mathutils import Vector
import json
import os, time

PATH = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(PATH, "atoms.json")) as in_file:
    atom_data = json.load(in_file)

def draw_substrate():
    scale = 1             #scales atomic radius by scale - does not change lattice constant
    a = 0.255            #lattice constant in nm
    a1 = a * 3.20432         # ####3,240692139

    dx=a1*cos(30)*1.0115836        # *1.0115836 to get nearest neighbour to 0.255
    dy=a1*sin(30)/sqrt(3)* 0.947583    #     ------------ " --------------

    d = (a1/sqrt(3)) * scale    / 7 #  original layer spacing
    overall_time = time.time()
#Iteration index, width of substrate drawn
    n = 100				  
    layers = 2            ### number of layers to draw ... >8gb(15Gb) for 3rd layer with n=50(120).. .
    smooth = True
    join = False
    link_to_scene = True

    verbose = True            # first level of verbose
    verbose2 = False        # second level of verbose

    do_square = False
    if do_square:
        array_mod = True        # adds standart modifier which will duplicate the sheet in x-direction
        array_mod_count = 2        # doubles the width, so it becomes square!
    else: array_mod = False
	
    mirror_y = False
# Add atom primitive
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    sphere.dimensions = [atom_data["Cu"]["radius"]* scale] * 3

    key = "Cu1"
    bpy.data.materials.new(name=key)
    bpy.data.materials[key].diffuse_color = (1, 0.638152, 0.252242)    #light brown
#    bpy.data.materials[key].diffuse_color = atom_data["Cu"]["color"]
    bpy.data.materials[key].diffuse_intensity = 0.7
    bpy.data.materials[key].specular_intensity = 0.2

    key = "Cu2"
    bpy.data.materials.new(name=key)
    bpy.data.materials[key].diffuse_color = (0.281, 0.183, 0.076)  #darker brown
    #bpy.data.materials[key].diffuse_color = atom_data["Cu"]["color"]
    bpy.data.materials[key].diffuse_intensity = 0.5
    bpy.data.materials[key].specular_intensity = 0
    bpy.data.materials[key].use_shadeless = False

    key = "Cu3"
    bpy.data.materials.new(name=key)
    bpy.data.materials[key].diffuse_color = (0.073, 0.049, 0.022)  #dark brown
#    bpy.data.materials[key].diffuse_color = atom_data["Cu"]["color"]
    bpy.data.materials[key].diffuse_intensity = 0.2
    bpy.data.materials[key].specular_intensity = 0
    bpy.data.materials[key].use_shadeless = False
###############################################################################################
    shapes = []
# build first layer
    print("Drawing layer 1:")
    layer_start_time = time.time()
    if do_square: 
        for i in range(n):
            for j in range(n):
                if verbose2:
                    print("row: ", j, " of ", n)
                row_start_time = time.time()
                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (2*i*dx,j*dy,0)
                atom_sphere.active_material = bpy.data.materials["Cu1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)

                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
                atom_sphere.active_material = bpy.data.materials["Cu1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)
                if verbose2: print("Atom: ",j)
            row_run_time = round((time.time() - row_start_time),2)
            if verbose: print("Time for row: ", i, " in layer I is ", row_run_time)
			
				
    else: 
        for j in range(n):
            if verbose2: print("row: ", i, " of ", n)
            row_start_time = time.time()
            for i in range(j):
                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (2*i*dx,j*dy,0)
                atom_sphere.active_material = bpy.data.materials["Cu1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)
	
                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
                atom_sphere.active_material = bpy.data.materials["Cu1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)
                if verbose2: print("Atom: ",i)
            row_run_time = round((time.time() - row_start_time),2)
            if verbose: print("Time for row: ", j, " in layer I is ", row_run_time)

    layer_runtime = round((time.time() - layer_start_time),2)
    print("--- Runtime: ", layer_runtime, " seconds --- for first layer")
	
## join single layer
    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]    #do not indent in for-selection loop
    print("Joining into single Layer...")
    start_time = time.time()
    bpy.ops.object.join()                #do not indent in for-selection loop
    if verbose: print("Time for joining: ", round((time.time() - start_time),2))
    if verbose: print("")
    bpy.ops.object.select_all(action='SELECT')    # select all objects (clean scene before?!)
##########################
    layer = bpy.context.object
    layer.name = "Layer 1"
    apply_list = []            # schreibt ertzeugte layer mit, damit man sie einzeln anwählen kann
    apply_list.append("Layer 1")
	
    print("Beginning stacking of layers")
    for i in range(1, layers):        # erzeugt kopier der ersten schicht
        start_time = time.time()
        print("copying layer")
        next_layer = layer.copy()
        if verbose:
            print("Time for copying: ", round((time.time() - start_time),2))

        print("copying layer data")
        next_layer.data = layer.data.copy()            #check if needed
        print("move layer by ",i,"*dx, ",i,"*dy/6, -",i,"*d")  #this has to be proper to apply correct array_modifier later on
        if i%3 == 0: next_layer.location += Vector((0, 0, -i*d))  # stack everyx 3rd above the first (fcc)
        if i%3 == 1: next_layer.location += Vector((1*dx, 1*dy/6, -i*d))
        if i%3 == 2: next_layer.location += Vector((2*dx, 2*dy/6, -i*d))

        print("Change material")
        materialname = "Cu" + str(i+1)
        if i > 2:
            materialname = "Cu3"        # use same color for layers > 3 (not visible from above)
        layername = "Layer " + str(i+1)
        next_layer.name = layername
        next_layer.active_material = bpy.data.materials[materialname]
        bpy.context.scene.objects.link(next_layer)
            
        if verbose: print("Add Layers to apply_list")
        apply_list.append(layername)


    if array_mod:
        for layer in apply_list:
            bpy.data.objects.get(layer).select = True
        bpy.context.scene.objects.active = shapes[0]
        print("Joining cloned Layers into one object...")
        start_time = time.time()
        bpy.ops.object.join()
        if verbose: print("Time for joining: ", round((time.time() - start_time),2))
        if verbose: print("")

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = array_mod_count
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0.9
        if verbose: print("Applying modifier 'ARRAY' ")
        start_time = time.time()
        bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier="Array")
        if verbose:
            print("Time for applying modifier: ",round((time.time() - start_time),2))
            print("")
			
    if mirror_y:
        for layer in apply_list:
            bpy.data.objects.get(layer).select = True
        bpy.context.scene.objects.active = shapes[0]
        print("Joining cloned Layers into one object...")
        start_time = time.time()
        bpy.ops.object.join()
        if verbose: print("Time for joining: ", round((time.time() - start_time),2))
        if verbose: print("")

        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = array_mod_count
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0.9
        if verbose: print("Applying modifier 'ARRAY' ")
        start_time = time.time()
        bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier="Array")
        if verbose:
            print("Time for applying modifier: ",round((time.time() - start_time),2))
            print("")

    print("Overall time: ",round((time.time() - overall_time),2))

#        for item in apply_list:            #Liste aller Layer die in der Schleife erzeugt wurden
#            layer_time = time.time()
#            if item in bpy.data.objects.keys():
#                if verbose: print("Found "+item+" in list of object-keys")
#                if verbose: print("Deselecting all")
#                bpy.ops.object.select_all(action='DESELECT')    # deselect all objects
#                if verbose: print("Selecting ", item)
#                bpy.data.objects.get(item).select = True
##            bpy.context.scene.objects.active = shape[0]
#            if verbose: print("Addind modifier 'ARRAY' ")
#            bpy.ops.object.modifier_add(type='ARRAY')
#            bpy.context.object.modifiers["Array"].count = array_mod_count
#            if verbose: print("Applying modifier 'ARRAY' ")
#            bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier="Array")
#            if verbose:
#                print("Time for applying modifier on ", item , round((time.time() - layer_time),2))
#                print("")
#
#        if verbose:
#            print("Total time for applying modifier: ", round((time.time() - start_time),2))

##########################

#    # copy first layer into second one
#    print("copying layer 1")
#    layer = bpy.context.object
#    layer2 = layer.copy()
#    layer2.data = layer.data.copy()            #check if needed
#    layer2.location += Vector((dx, dy/6, -d))
#    layer2.active_material = bpy.data.materials["Cu2"]
#    bpy.context.scene.objects.link(layer2)
#    # copy second layer into third one
#    print("copying layer 2")
#    layer3 = layer2.copy()
#    layer3.data = layer2.data.copy()        #check if needed
#    layer3.location += Vector((dx, dy/6, -d))
#    layer3.active_material = bpy.data.materials["Cu3"]
#    bpy.context.scene.objects.link(layer3)

def clear_scene():
# If the starting cube is there, remove it
    remove_list = ["Cube", "Camera", "Lamp"]
    for item in remove_list:
        if item in bpy.data.objects.keys():
            bpy.data.objects.get(item).select = True
        bpy.ops.object.delete()

# Runs the method
if __name__ == "__main__":
    clear_scene()
    draw_substrate()
    bpy.context.scene.update()
#  render_all_cameras("/home/ga32xan/git-working-dir/blender-chemicals/substrate-to-blender")