"""Derive six editable roadmap illustrations from the existing Blender atlas."""
import bpy, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'handbook/downloads/farm-visual-atlas.blend'))
originals=list(bpy.data.scenes)
ink=bpy.data.materials['Unlit annotation']
def text(body,loc,size=.012):
 c=bpy.data.curves.new(body,'FONT');c.body=body;c.size=size;c.align_x='CENTER'
 o=bpy.data.objects.new(body,c);bpy.context.scene.collection.objects.link(o);o.location=loc;o.rotation_euler=bpy.context.scene.camera.rotation_euler;o.data.materials.append(ink)
def create(name,source,title,subtitle):
 s=bpy.data.scenes[source].copy();s.name=name;bpy.context.window.scene=s
 for ob in list(s.objects):
  if ob.type=='FONT':s.collection.objects.unlink(ob)
 original_camera=s.camera;cam=original_camera.copy();cam.data=original_camera.data.copy();s.collection.objects.link(cam);s.collection.objects.unlink(original_camera);s.camera=cam
 if 'workstation' in source:cam.data.ortho_scale*=1.5
 scale=cam.data.ortho_scale
 for t,y,size in [(title,.292,.025),(subtitle,-.30,.014)]:text(t,cam.location+cam.rotation_euler.to_quaternion()@Vector((0,scale*y,-.05)),scale*size)
 s.cycles.samples=16
 return s
def finish(s,file):
 for ob in s.objects:
  if ob.type=='FONT' and not ob.get('screen_label'):ob.hide_render=True
 s.render.filepath=str(ROOT/'handbook/assets/blender'/file);bpy.ops.render.render(write_still=True);s.render.filepath='//../assets/blender/'+file
def screen_label(body,x,z,size=.016):
 c=bpy.data.curves.new(body,'FONT');c.body=body;c.size=size;c.align_x='CENTER'
 o=bpy.data.objects.new(body,c);bpy.context.scene.collection.objects.link(o);o.location=(x,.106,z);o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(ink);o['screen_label']=True
s=create('Roadmap / simulator','08 Three prepared plates','SIMULATOR / VIRTUAL TRAYS','Model only. Simulated responses must remain separate from physical outcomes.')
text('TRAY A',(-.34,-.245,.03),.018);text('TRAY B',(0,-.245,.03),.018);text('INTERRUPT / REPLAY',(.34,-.245,.03),.018)
finish(s,'roadmap-simulator.png')
s=create('Roadmap / exception viewer','15 Software evidence workstation','EXCEPTION VIEWER / PAUSED','Interface concept. A lost acknowledgement must not trigger another pour.')
text('DELIVERY UNKNOWN',(0,.045,.29),.016);text('HUMAN REVIEW',(.21,-.08,.045),.01)
for ob in list(s.objects):
 if ob.name.startswith(('Recorded image tile','Evidence row')):s.collection.objects.unlink(ob)
screen_label('PAUSED',0,.20,.024);screen_label('Delivery unknown',0,.165,.016);screen_label('Review before continuing',0,.125,.011)
finish(s,'roadmap-review.png')
s=create('Roadmap / camera fault','Care / inspect','CAMERA COVERAGE / UNKNOWN','A blocked view cannot establish that the watering area is clear.')
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,.025,.14));ob=bpy.context.object;ob.name='Illustrative camera obstruction';ob.dimensions=(.075,.004,.07);ob.data.materials.append(bpy.data.materials['Purchased dark housing'])
finish(s,'roadmap-occlusion.png')
s=create('Roadmap / model evaluation','15 Software evidence workstation','MODEL EVALUATION / SHADOW MODE','Concept only. Models review evidence; local checks retain control.')
text('RULES     JEV     ASTRA',(0,.045,.29),.015);text('COMPARE OUTCOMES',(.21,-.08,.045),.009)
for x,t in [(-.09,'RULES'),(0,'JEV'),(.09,'ASTRA')]:screen_label(t,x,.19,.012)
finish(s,'roadmap-models.png')
s=create('Roadmap / action record','15 Software evidence workstation','ACTION RECORD','Illustrative local record')
finish(s,'roadmap-record.png')
s=create('Roadmap / current hardware','02 Connected workbench','CURRENT HARDWARE','Light sensor only')
for ob in list(s.objects):
 if ob.type=='MESH' and ob.location.x>.19 and -.11<ob.location.y<-.04:s.collection.objects.unlink(ob)
finish(s,'roadmap-hardware.png')
for s in originals:bpy.data.scenes.remove(s)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'handbook/downloads/software-roadmap-scenes.blend'),compress=True)
