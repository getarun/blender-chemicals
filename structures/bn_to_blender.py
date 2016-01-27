#!/usr/bin/env python

import bpy
from math import sin,cos,sqrt
from mathutils import Vector
import json
import os, time

# Get path of this file (useful when this script is imported)
PATH = os.path.dirname(os.path.realpath(__file__))

# Atomic radii from wikipedia, scaled to Blender radii (C = 0.4 units)
# http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page)
# Atomic colors from cpk
# http://jmol.sourceforge.net/jscolors/
with open(os.path.join(PATH, "atoms.json")) as in_file:
	atom_data = json.load(in_file)


def draw_BN():
# lattice dimension ... check scaling "C
	a = 0.25			  #a in nm
	a1 = a * 3.2792 / 1.77205 #/ 1.77205 1.9111# #correct spacings for correct nearest neighbour distance to be "a"

	dx=a1*cos(30)*1.0115836
	dy=a1*sin(30)/sqrt(3)* 0.947583	

#Iteration index, width of substrate drawn
	n = 90
	scale = 1			#scales atomic radius jsondata*scale
	add_vdW_balls = True
	smooth = False
	join = False
	shapes = []
	verbose = True
	do_square = True

# Add atom samples and hide them
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereN = bpy.context.object
	sphereN.dimensions = [atom_data["N"]["radius"]* scale] * 3
#	sphereN.hide = 1

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereNvdW = bpy.context.object
	sphereNvdW.dimensions = [atom_data["N"]["vdWradius"]* scale] * 3
#	sphereNvdW.hide = 1

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereB = bpy.context.object
	sphereB.dimensions = [atom_data["B"]["radius"]* scale] * 3
#	sphereB.hide = 1

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereBvdW = bpy.context.object
	sphereBvdW.dimensions = [atom_data["B"]["vdWradius"]* scale] * 3
#	sphereBvdW.hide = 1
######################

	#the radius from atoms.json is written in pm and only checked for B,N,Cu
	key = "B"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	bpy.data.materials[key].specular_intensity = 0.2
	key = "BvdW"	#add translucent sphere to indicate vanderWaalsradius
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["B"]["color"]
	bpy.data.materials[key].use_transparency = 1
	bpy.data.materials[key].transparency_method = "RAYTRACE"
	bpy.data.materials[key].alpha=0.3
##################
	key = "N"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	key = "NvdW"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["N"]["color"]
	bpy.data.materials[key].use_transparency  = 1
	bpy.data.materials[key].transparency_method = "RAYTRACE"
	bpy.data.materials[key].alpha=0.3

# remove special atoms to achieve BN layer
	delete_list_1 = []
	for i in range(n):
		delete_list_1.append(2+3*i)
	delete_list_2 = []
	for j in range(n):
		delete_list_2.append(3*j)

	layer_start_time = time.time()
	if do_square: 
		for i in range(3*n):
			for j in range(n):
				if i not in delete_list_1:
					if i%3==0:		#Draw B atoms
						atom_sphere = sphereB.copy()
						atom_sphere.data = sphereB.data.copy()
						atom_sphere.location = (2*i*dx,j*dy,0)
						atom_sphere.active_material = bpy.data.materials["B"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereBvdW.copy()
							atom_sphere.data = sphereBvdW.data.copy()
							atom_sphere.location = (2*i*dx,j*dy,0)
							atom_sphere.active_material = bpy.data.materials["BvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
					if i%3==1:
						atom_sphere = sphereN.copy()
						atom_sphere.data = sphereN.data.copy()
						atom_sphere.location = (2*i*dx,j*dy,0)
						atom_sphere.active_material = bpy.data.materials["N"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereNvdW.copy()
							atom_sphere.data = sphereNvdW.data.copy()
							atom_sphere.location = (2*i*dx,j*dy,0)
							atom_sphere.active_material = bpy.data.materials["NvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
				if i not in delete_list_2:
					if i%3==1:
						atom_sphere = sphereB.copy()
						atom_sphere.data = sphereB.data.copy()
						atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
						atom_sphere.active_material = bpy.data.materials["B"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereBvdW.copy()
							atom_sphere.data = sphereBvdW.data.copy()
							atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
							atom_sphere.active_material = bpy.data.materials["BvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
							
					if i%3==2:
						atom_sphere = sphereN.copy()
						atom_sphere.data = sphereN.data.copy()
						atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
						atom_sphere.active_material = bpy.data.materials["N"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereNvdW.copy()
							atom_sphere.data = sphereNvdW.data.copy()
							atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
							atom_sphere.active_material = bpy.data.materials["NvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
		layer_runtime = round((time.time() - layer_start_time),2)
		print("--- Runtime: ", layer_runtime, " seconds --- for first layer")
	else:						
		for j in range((0,int(n/4)+1,1)):		#range(1,n) for one N-terminated edge
			if verbose2: print("row: ", i, " of ", n)
			row_start_time = time.time()
			for i in range(-j,(n-j)+2,1):	#range(start,stop,increment) range(i,n+i) for raute along ?????
				if i not in delete_list_1:
					if i%3==0:
						atom_sphere = sphereB.copy()
						atom_sphere.data = sphereB.data.copy()
						atom_sphere.location = (2*i*dx,j*dy,0)
						atom_sphere.active_material = bpy.data.materials["B"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereBvdW.copy()
							atom_sphere.data = sphereBvdW.data.copy()
							atom_sphere.location = (2*i*dx,j*dy,0)
							atom_sphere.active_material = bpy.data.materials["BvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
					if i%3==1:
						atom_sphere = sphereN.copy()
						atom_sphere.data = sphereN.data.copy()
						atom_sphere.location = (2*i*dx,j*dy,0)
						atom_sphere.active_material = bpy.data.materials["N"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereNvdW.copy()
							atom_sphere.data = sphereNvdW.data.copy()
							atom_sphere.location = (2*i*dx,j*dy,0)
							atom_sphere.active_material = bpy.data.materials["NvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
				if i not in delete_list_2:
					if i%3==1:
						atom_sphere = sphereB.copy()
						atom_sphere.data = sphereB.data.copy()
						atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
						atom_sphere.active_material = bpy.data.materials["B"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereBvdW.copy()
							atom_sphere.data = sphereBvdW.data.copy()
							atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
							atom_sphere.active_material = bpy.data.materials["BvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
							
					if i%3==2:
						atom_sphere = sphereN.copy()
						atom_sphere.data = sphereN.data.copy()
						atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
						atom_sphere.active_material = bpy.data.materials["N"]
						bpy.context.scene.objects.link(atom_sphere)
						shapes.append(atom_sphere)
						if add_vdW_balls:
							atom_sphere = sphereNvdW.copy()
							atom_sphere.data = sphereNvdW.data.copy()
							atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
							atom_sphere.active_material = bpy.data.materials["NvdW"]
							bpy.context.scene.objects.link(atom_sphere)
							shapes.append(atom_sphere)
				row_run_time = round((time.time() - row_start_time),2)
				if verbose: print("Time for row: ", j, " is ", row_run_time)

		layer_runtime = round((time.time() - layer_start_time),2)
		print("--- Runtime: ", layer_runtime, " seconds --- for first layer")

	if smooth:
		for shape in shapes:
			shape.select = True
		bpy.context.scene.objects.active = shapes[0]
		bpy.ops.object.shade_smooth()
		if join: bpy.ops.object.join()

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
	draw_BN()
#	add_camera()
	bpy.context.scene.update()
