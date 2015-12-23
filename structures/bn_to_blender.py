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
	a = 0.255				#a in nm
	a1 = a * 3.55	/ 1.095445	#sqrt(dx**2+dy**2)=sqrt(5/6) #correct spacings for correct nearest 						neighbour distance to be "a"

	dx=a1*cos(30)
	dy=a1*sin(30)/sqrt(3)	

#Iteration index, width of substrate drawn
	n = 30
	scale = 1
	add_vdW_balls = True
	shapes = []

# Add atom samples
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereN = bpy.context.object
	sphereN.dimensions = [atom_data["N"]["radius"]* scale] * 3

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereNvdW = bpy.context.object
	sphereNvdW.dimensions = [atom_data["N"]["vdWradius"]* scale] * 3

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereB = bpy.context.object
	sphereB.dimensions = [atom_data["B"]["radius"]* scale] * 3

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphereBvdW = bpy.context.object
	sphereBvdW.dimensions = [atom_data["B"]["vdWradius"]* scale] * 3
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

	key = "N"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	key = "NvdW"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["N"]["color"]
	bpy.data.materials[key].use_transparency  = 1
	bpy.data.materials[key].transparency_method = "RAYTRACE"
	bpy.data.materials[key].alpha=0.3


	delete_list_1 = []
	for i in range(n):
		delete_list_1.append(2+3*i)
	delete_list_2 = []
	for j in range(n):
		delete_list_2.append(3*j)
# build first layer

	for i in range(n):

		for j in range(n):

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
				bpy.ops.object.parent_set(type='OBJECT')


    # Smooth and join molecule shapes
	for shape in shapes:
		shape.select = True
	bpy.context.scene.objects.active = shapes[0]
	bpy.ops.object.shade_smooth()
	bpy.ops.object.join()
############################################################
	bpy.ops.object.select_all(action='DESELECT')
	sphere.select = True
	bpy.ops.object.delete()

# Center object origin to geometry
	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

	bpy.context.scene.update()
def add_camera():
	import bpy
	tx = 0.0
	ty = 0.0
	tz = 5.0

	rx = 0.0
	ry = 0.0
	rz = 0.0

	fov = 50.0

	pi = 3.14159265

	scene = bpy.data.scenes["Scene"]

	# Set render resolution
	scene.render.resolution_x = 1080
	scene.render.resolution_y = 920

	# Set camera fov in degrees
	scene.camera.data.angle = fov*(pi/180.0)

	# Set camera rotation in euler angles
	scene.camera.rotation_mode = 'XYZ'
	scene.camera.rotation_euler[0] = rx*(pi/180.0)
	scene.camera.rotation_euler[1] = ry*(pi/180.0)
	scene.camera.rotation_euler[2] = rz*(pi/180.0)

	# Set camera translation
	scene.camera.location.x = tx
	scene.camera.location.y = ty
	scene.camera.location.z = tz

# Runs the method
if __name__ == "__main__":
	draw_BN()
	add_camera()
