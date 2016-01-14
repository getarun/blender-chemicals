#!/usr/bin/env python

import bpy
from math import sin,cos,sqrt
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


def draw_BN():
# lattice dimension ... check scaling "C
	a = 0.255			  #a in nm
	a1 = a * 3.517 / 1.9111 / 1.77205 #sqrt(dx**2+dy**2)=sqrt(5/6) #correct spacings for correct nearest neighbour distance to be "a"

	dx=a1*cos(30)
	dy=a1*sin(30)/sqrt(3)	

#Iteration index, width of substrate drawn
	n = 50
	scale = 1			#scales atomic radius jsondata*scale
	add_vdW_balls = True
	smooth = False
	join = False
	shapes = []

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

	for i in range(n):		#range(1,n) for one N-terminated edge
		for j in range(round(n/2)):	#range(start,stop,increment) range(i,n+i) for raute along
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
#				bpy.ops.object.parent_set(type='OBJECT')

#delete created sample atoms
#	remove_list = ["Sphere", "Sphere.001", "Sphere.002"]
#	for item in remove_list:
#		if item in bpy.data.objects.keys():
#			bpy.data.objects.get(item).select = True
#		bpy.ops.object.delete()

# Smooth and join molecule shapes
	if smooth:
		for shape in shapes:
			shape.select = True
		bpy.context.scene.objects.active = shapes[0]
		bpy.ops.object.shade_smooth()
		if join: bpy.ops.object.join()

############################################################
#	bpy.ops.object.select_all(action='DESELECT')
#	sphere.select = True
#	bpy.ops.object.delete()

# Center object origin to geometry
#	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

#	bpy.context.scene.update()

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
