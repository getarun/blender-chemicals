#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import bpy
from math import sin,cos,sqrt
from mathutils import Vector
import json
import os, time
## Keep atoms.json in same dir as the script file
with open("atoms.json") as in_file:
    atom_data = json.load(in_file)

def draw_substrate():
    scale = 1             #scales atomic radius by scale - does not change lattice constant
    element = "Cu"        # changes lattice constant as in atoms.json-file, Ag, Cu implemented already
    a = atom_data[element]["fcc-const"]
    a1 = a * 3.20432      # scale to 1bu = 1nm
    hexagonal = False
    square = False
    rect = True
    if hexagonal:       # 111
        a1 *= sqrt(2)/2        
        dx=a1*cos(30)*1.0115836        # *1.0115836 to get nearest neighbour to 0.255
        dy=a1*sin(30)/sqrt(3)* 0.947583    #     correct angle
        d = (a1/sqrt(3)) * scale    / 5 #  original layer spacing / 5 to make it more realistic
        do_square = False           #   set creation method for the for-loops
        different_stacking = 3      #default: 3
    if square:          # 100
        a1 *= sqrt(2)/2       
        dx = a1 * 0.312079648       #   match correct spacing
        dy = a1 * 0.312079648
        d = (a1/sqrt(1)) * scale    / 5 #  original layer spacing
        do_square = True
        different_stacking = 2      #default: 2
    if rect:            #110
        a2 = a1        
        a1 *= sqrt(2)/2    
            
        dx = a1 * 0.312079648       #   match correct spacing
        dy = a2 * 0.312079648
        d = (a1/sqrt(2)) * scale    / 5 #  original layer spacing
        do_square = True
        different_stacking = 2      #default: 2

    overall_time = time.time()
#Iteration index, width of substrate drawn

    n = 50		  # resembles atoms along close packed direction of moire cell created when do_square= False
    layers = different_stacking            ### number of layers to draw ... >8gb(15Gb) for 3rd layer with n=50(120).. .
    smooth = True
    join = True     #set to false if you want to check distances for debugging purposes
    link_to_scene = True

    verbose = True            # first level of verbose
    verbose2 = True        # second level of verbose

    if do_square:
        array_mod = False        # adds standart modifier which will duplicate the sheet in x-direction
        array_mod_count = 2        # doubles the width, so it becomes square!
    else: array_mod = False
	
    mirror_y = False		#does not work as expected ... wrong mirror plane
# Add atom primitive
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    sphere.dimensions = [atom_data[element]["radius"]* scale] * 3
    for i in range(1,different_stacking+1):         #start labelling with "Cu"1
        key = element + str(i)
        if verbose2: print("Creating Material", key)
        bpy.data.materials.new(name=key)
        bpy.data.materials[key].diffuse_color = (pow(atom_data[element]["color"][0]*0.6,i), pow(atom_data[element]["color"][1]*0.6,i), pow(atom_data[element]["color"][2]*0.6,i))    
#        bpy.data.materials[key].diffuse_color = atom_data[element]["color"]
        bpy.data.materials[key].diffuse_intensity = 0.7 - 0.2*i
        bpy.data.materials[key].specular_intensity = 0.2 - 0.1*i

###############################################################################################
    shapes = []
# build first layer
    print("Drawing layer 1:")
    layer_start_time = time.time()

    if rect: 
        for i in range(n):
            print("Drawing row: ",i)
            row_start_time = time.time()
            for j in range(n):
                if verbose2: print("Row: ",i," -- Atom: ", j, " of ", n)

                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (i*dx,j*dy,0)
                atom_sphere.active_material = bpy.data.materials[element + "1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)

            row_run_time = round((time.time() - row_start_time),2)
            if verbose: print("Time for row: ", i, " is ", row_run_time)
    

    if square: 
        for i in range(n):
            row_start_time = time.time()
            for j in range(n):
                if verbose2: print("Row: ",i," -- Atom: ", j, " of ", n)

                atom_sphere = sphere.copy()
                atom_sphere.data = sphere.data.copy()
                atom_sphere.location = (i*dx,j*dy,0)
                atom_sphere.active_material = bpy.data.materials[element + "1"]
                bpy.context.scene.objects.link(atom_sphere)
                shapes.append(atom_sphere)

            row_run_time = round((time.time() - row_start_time),2)
            if verbose: print("Time for row: ", i, " in layer I is ", row_run_time)
			
				
    if hexagonal: 
        if do_square:
            for i in range(n):
                print("Drawing row: ",i)
                row_start_time = time.time()
                for j in range(n):
                    if verbose2: print("Row: ",i," -- Atom: ", j, " of ", n)

                    atom_sphere = sphere.copy()
                    atom_sphere.data = sphere.data.copy()
                    atom_sphere.location = (2*i*dx,j*dy,0)
                    atom_sphere.active_material = bpy.data.materials[element + "1"]
                    bpy.context.scene.objects.link(atom_sphere)
                    shapes.append(atom_sphere)

                    atom_sphere = sphere.copy()
                    atom_sphere.data = sphere.data.copy()
                    atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
                    atom_sphere.active_material = bpy.data.materials[element + "1"]
                    bpy.context.scene.objects.link(atom_sphere)
                    shapes.append(atom_sphere)
                row_run_time = round((time.time() - row_start_time),2)
                if verbose: print("Time for row: ", i, " is ", row_run_time)
        else:
            for j in range(0,int(n/2)+1,1):					# for j in range(0,int(n/2),1): raute along close packed row
                if verbose2: print("row: ", j, " of ", n)
                row_start_time = time.time()
                for i in range(-j,(n-j)+2,1):				# for i in range(-j,n-j,1): raute along close packed row
                    if verbose2: print("Row: ",i," -- Atom: ", j, " of ", n)
                    atom_sphere = sphere.copy()
                    atom_sphere.data = sphere.data.copy()
                    atom_sphere.location = (2*i*dx,j*dy,0)
                    atom_sphere.active_material = bpy.data.materials[element + "1"]
                    bpy.context.scene.objects.link(atom_sphere)
                    shapes.append(atom_sphere)
	
                    atom_sphere = sphere.copy()
                    atom_sphere.data = sphere.data.copy()
                    atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
                    atom_sphere.active_material = bpy.data.materials[element + "1"]
                    bpy.context.scene.objects.link(atom_sphere)
                    shapes.append(atom_sphere)
                    if verbose2: print("Atom: ",i)
                row_run_time = round((time.time() - row_start_time),2)
                if verbose: print("Time for row: ", j, " is ", row_run_time)

    layer_runtime = round((time.time() - layer_start_time),2)
    print("--- Runtime: ", layer_runtime, " seconds --- for first layer")
	
## join single layer
    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]    #do not indent in for-selection loop
    if join:
        print("Joining into single Layer...")
        start_time = time.time()
        bpy.ops.object.join()                #do not indent in for-selection loop
        if verbose: print("Time for joining: ", round((time.time() - start_time),2))
        if verbose: print("")
    bpy.ops.object.select_all(action='SELECT')    # select all objects (cleaned scene before?!)
##########################
# the following only works if join = True
    if not join: 
        print("!!!!!!!!!enable join to build several layers!!!!!!!!!")
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

        if hexagonal:
            print("copying layer data")
            next_layer.data = layer.data.copy()            #check if needed
            if i%3 == 0: 
                next_layer.location += Vector((0, 0, -i*d))  
            if i%3 == 1: 
                next_layer.location += Vector((2*dx, 2*dy/6, -i*d))
            if i%3 == 2: 
                next_layer.location += Vector((1*dx, 1*dy/6, -i*d)) #first stacked layer, i.e.1%3=2
               
            print("Change material")
            materialname = element + str(i%3+1)   # Layer1 already created out of single atoms, start at 2
     #       if i > 2:
     #           materialname = "Cu3"        # use same color for layers > 3 (not visible from above)
            layername = "Layer " + str(i+1)
            next_layer.name = layername
            next_layer.active_material = bpy.data.materials[materialname]
            bpy.context.scene.objects.link(next_layer)

        if square|rect:
            print("copying layer data")
            next_layer.data = layer.data.copy()            #check if needed
            if i%2 == 0: 
                next_layer.location += Vector((0, 0, -i*d))  
            if i%2 == 1: 
                next_layer.location += Vector((dx/2, dy/2, -i*d))
               
            print("Change material")
            materialname = element + str(i%2+1)   # Layer1 already created out of single atoms, start at 2
     #       if i > 2:
     #           materialname = "Cu3"        # use same color for layers > 3 (not visible from above)
            layername = "Layer " + str(i+1)
            next_layer.name = layername
            next_layer.active_material = bpy.data.materials[materialname]
            bpy.context.scene.objects.link(next_layer)
        
#################            
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
