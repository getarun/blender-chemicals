###############################################################

def render_all_cameras(path):
	import os
	scene = bpy.context.scene
	for ob in scene.objects:
		if ob.type == 'CAMERA':
			bpy.context.scene.camera = ob
			print('Set camera %s' % ob.name )
			file = os.path.join(path, ob.name )
			bpy.context.scene.render.filepath = file
			bpy.ops.render.render( write_still=True )	

###############################################################

def antiphase_boundary():
#	copy and translate by absoltute (0,0,0) antiphase_boundary_I
#	copy and translate
#### dx = 0,810173035
#### dy = 0,935507239

## 4*dx = 3,24069214
