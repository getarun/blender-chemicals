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


def draw_substrate():
# lattice dimension ... check scaling "C
	a = 2.55
	d= 3.61/sqrt(3)
#Iteration index, width of substrate drawn
	n = 5
	scale = 1
	shapes = []

# Add atom primitive
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphere = bpy.context.object
	sphere.dimensions = [atom_data["Cu"]["radius"]* 2 * scale] * 3
	
	key = "Cu"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	bpy.data.materials[key].specular_intensity = 0.2	
	key = "Ag"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	bpy.data.materials[key].specular_intensity = 0.2	
	key = "Fe"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data[key]["color"]
	bpy.data.materials[key].specular_intensity = 0.2
	
# build first layer

	for i in range(n):

		for j in range(n):

			dx=a*cos(30)
			dy=a*sin(30)/sqrt(3)	
			
			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx,j*dy,0)
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
			bpy.ops.object.parent_set(type='OBJECT')

			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)

# build second layer
	for i in range(n):

		for j in range(n):

			dx=a*cos(30)
			dy=a*sin(30)/sqrt(3)	
			
			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx,j*dy+dy/6,d)
			atom_sphere.active_material = bpy.data.materials["Ag"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
			bpy.ops.object.parent_set(type='OBJECT')

			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx+dx,j*dy+dy/2+dy/6,d)
			atom_sphere.active_material = bpy.data.materials["Ag"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
	#bpy.ops.object.select_all(action='SELECT')

# build third layer
	for i in range(n):

		for j in range(n):

			dx=a*cos(30)
			dy=a*sin(30)/sqrt(3)	
			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx+dx,j*dy+2*dy/6,2*d)
			atom_sphere.active_material = bpy.data.materials["Fe"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
			bpy.ops.object.parent_set(type='OBJECT')

			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx+dx+dx,j*dy+dy/2+2*dy/6,2*d)
			atom_sphere.active_material = bpy.data.materials["Fe"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
	#bpy.ops.object.select_all(action='SELECT')

    # Smooth and join molecule shapes
	for shape in shapes:
		shape.select = True
	bpy.context.scene.objects.active = shapes[0]
	bpy.ops.object.shade_smooth()

# Center object origin to geometry
	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

def add_light(tx, ty, tz, style):

	scene = bpy.context.scene

	# Create new lamp datablock
	lamp_data = bpy.data.lamps.new(name="New Lamp", type=style)

	# Create new object with our lamp datablock
	lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)

	# Link lamp object to the scene so it'll appear in this scene
	scene.objects.link(lamp_object)

	# Place lamp to a specified location
	lamp_object.location = (tx, ty, tz)

	# And finally select it make active
	lamp_object.select = True
	scene.objects.active = lamp_object
def clear_scene():
# If the starting cube is there, remove it
	if "Cube" in bpy.data.objects.keys():
		bpy.data.objects.get("Cube").select = True
	if "Lamp" in bpy.data.objects.keys():
		bpy.data.objects.get("Lamp").select = True
	bpy.ops.object.delete()

def add_camera(tx,ty,tz,rx,ry,rz):
	import bpy
#	tx = 0.0
#	ty = 0.0
#	tz = 30.0

#	rx = 0.0
#	ry = 0.0
#	rz = 0.0

	fov = 25.0

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
	clear_scene()	
	draw_substrate()

	add_light(2,-3,10,"HEMI")
	add_light(0,0,12,"POINT")
	add_light(0,-10,13,"POINT")
	add_light(10,0,12,"POINT")
	add_light(10,-10,12,"POINT")

	add_camera(0,0,30,0,0,0)
	bpy.context.scene.update()