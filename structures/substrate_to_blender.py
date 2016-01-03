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

###############################################################
def draw_substrate():
# lattice dimension ... check scaling "C
	scale = 1 			#scales atomic radius by scale - does not change lattice constant

	a = 0.25			#lattice constant in nm
	a1 = a * 3.55	/ 1.095445	#sqrt(dx**2+dy**2)=sqrt(5/6)=1.095445
 #correct spacings for correct nearest neighbour distance to be a

	dx=a1*cos(30)
	dy=a1*sin(30)/sqrt(3)	

	d= (3.61/sqrt(3)) * scale / 7	#reduce original layer spacing

	layers = 2			### number of layers to draw
#Iteration index, width of substrate drawn
	n = 50

	shapes = []

# Add atom primitive
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_uv_sphere_add()
	sphere = bpy.context.object
	sphere.dimensions = [atom_data["Cu"]["radius"]* scale] * 3
	
	key = "Cu1"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["Ca"]["color"]
	bpy.data.materials[key].specular_intensity = 0.2	
	
	key = "Cu2"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["Au"]["color"]
	bpy.data.materials[key].specular_intensity = 0.2	

	key = "Cu3"
	bpy.data.materials.new(name=key)
	bpy.data.materials[key].diffuse_color = atom_data["Cu"]["color"]
	bpy.data.materials[key].specular_intensity = 0.2	
# build first layer beneath other ones
	for i in range(n):

		for j in range(n):

			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx,j*dy,0)
			atom_sphere.active_material = bpy.data.materials["Cu1"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)
			bpy.ops.object.parent_set(type='OBJECT')

			atom_sphere = sphere.copy()
			atom_sphere.data = sphere.data.copy()
			atom_sphere.location = (2*i*dx+dx,j*dy+dy/2,0)
			atom_sphere.active_material = bpy.data.materials["Cu1"]
			bpy.context.scene.objects.link(atom_sphere)
			shapes.append(atom_sphere)

	if layers > 1: # build second layer
		for i in range(n):

			for j in range(n):
			
				atom_sphere = sphere.copy()
				atom_sphere.data = sphere.data.copy()
				atom_sphere.location = (2*i*dx+dx,j*dy+dy/6,-d)
				atom_sphere.active_material = bpy.data.materials["Cu2"]
				bpy.context.scene.objects.link(atom_sphere)
				shapes.append(atom_sphere)
				bpy.ops.object.parent_set(type='OBJECT')

				atom_sphere = sphere.copy()
				atom_sphere.data = sphere.data.copy()
				atom_sphere.location = (2*i*dx+dx+dx,j*dy+dy/2+dy/6,-d)
				atom_sphere.active_material = bpy.data.materials["Cu2"]
				bpy.context.scene.objects.link(atom_sphere)
				shapes.append(atom_sphere)
		#bpy.ops.object.select_all(action='SELECT')

	if layers > 2: # build third layer
		for i in range(n):

			for j in range(n):

				dx=a*cos(30)
				dy=a*sin(30)/sqrt(3)	
				atom_sphere = sphere.copy()
				atom_sphere.data = sphere.data.copy()
				atom_sphere.location = (2*i*dx+dx+dx,j*dy+2*dy/6,-2*d)
				atom_sphere.active_material = bpy.data.materials["Cu3"]
				bpy.context.scene.objects.link(atom_sphere)
				shapes.append(atom_sphere)
				bpy.ops.object.parent_set(type='OBJECT')

				atom_sphere = sphere.copy()
				atom_sphere.data = sphere.data.copy()
				atom_sphere.location = (2*i*dx+dx+dx+dx,j*dy+dy/2+2*dy/6,-2*d)
				atom_sphere.active_material = bpy.data.materials["Cu3"]
				bpy.context.scene.objects.link(atom_sphere)
				shapes.append(atom_sphere)
		#bpy.ops.object.select_all(action='SELECT')

    # Smooth and join molecule shapes
	for shape in shapes:
		shape.select = True
	bpy.context.scene.objects.active = shapes[0]
	bpy.ops.object.shade_smooth()
	bpy.ops.object.join()
# Center object origin to geometry
	bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

###############################################################
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

###############################################################
def clear_scene():
# If the starting cube is there, remove it
	if "Cube" in bpy.data.objects.keys():
		bpy.data.objects.get("Cube").select = True
	if "Lamp" in bpy.data.objects.keys():
		bpy.data.objects.get("Lamp").select = True
	if "Camera" in bpy.data.objects.keys():
		bpy.data.objects.get("Lamp").select = True
	bpy.ops.object.delete()

###############################################################
def add_camera(tx,ty,tz,rx,ry,rz,label):
	import bpy

	fov = 25.0
	pi = 3.14159265

#	angle= 50
#	axis=(1,0,0)

	scene = bpy.context.scene
	# Create new lamp datablock
	camera_data = bpy.data.cameras.new(name=label)
	# Create new object with our lamp datablock
	camera_object = bpy.data.objects.new(name=label, object_data=camera_data)
	# Link lamp object to the scene so it'll appear in this scene
	scene.objects.link(camera_object)
	# Place lamp to a specified location
	camera_object.location = (tx, ty, tz)

	# And finally select it and make it active
	camera_object.select = True
	scene.objects.active = camera_object

#	obj_types = ['CAMERA']
#	for obj in bpy.data.objects:
#		if obj.type in obj_types:
#			if len(obj.keys()) > 1:
#		    # First item is _RNA_UI
#				print("Object",obj.name,"custom properties:")
#				for K in obj.keys():
#					if K not in '_RNA_UI':
#						print( K , "-" , obj[K] )
#			else:
#				print("Only has RNA_UI property")



###############################################################
#	scene = bpy.data.scenes["Scene"]

	# Set render resolution
#	scene.render.resolution_x = 1080
#	scene.render.resolution_y = 920

	# Set camera fov in degrees
#	scene.camera.data.angle = fov*(pi/180.0)

	# Set camera rotation in euler angles
#	scene.camera.rotation_mode = 'XYZ'
#	scene.camera.rotation_euler[0] = rx*(pi/180.0)
#	scene.camera.rotation_euler[1] = ry*(pi/180.0)
#	scene.camera.rotation_euler[2] = rz*(pi/180.0)

	# Set camera translation
#	scene.camera.location.x = tx
#	scene.camera.location.y = ty
#	scene.camera.location.z = tz
#	scene.objects.link(camera)

###############################################################

def render_all_cameras(path):

	scene = bpy.context.scene
	for ob in scene.objects:
		if ob.type == 'CAMERA':
			bpy.context.scene.camera = ob
			print('Set camera %s' % ob.name )
			file = os.path.join(path, ob.name )
			bpy.context.scene.render.filepath = file
			bpy.ops.render.render( write_still=True )	

###############################################################
# Runs the method
if __name__ == "__main__":
	clear_scene()	
	draw_substrate()

	add_light(2,-3,10,"HEMI")
	add_light(0,0,12,"POINT")
	add_light(0,-10,13,"POINT")
	add_light(10,0,12,"POINT")
	add_light(10,-10,12,"POINT")

	add_camera(3,-4,20,0,0,0,"cam1")
	add_camera(2,5,5,-90,180,0,"cam2")
	bpy.context.scene.update()
	render_all_cameras("/home/domenik/git-working-dir/blender-chemicals/substrate-to-blender")
