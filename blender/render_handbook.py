"""Blender-only illustrative renders. Run with --background --factory-startup --python.
Actual STL imports retain creator geometry; electronics, cables and robot grips are
illustrative, not engineering geometry. No output from this script is print-ready.
"""
import bpy, math, random, tempfile, zipfile
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'handbook/assets/blender';OUT.mkdir(parents=True,exist_ok=True)
TMP=Path(tempfile.mkdtemp(prefix='farm-blender-'))
for f in ['planter-source-stls.zip','tool-prototypes-v2.zip']:
 with zipfile.ZipFile(ROOT/'handbook/downloads'/f) as z:z.extractall(TMP)
for s in list(bpy.data.scenes):
 if len(bpy.data.scenes)>1:bpy.data.scenes.remove(s)
bpy.context.scene.name='Unused'

def mat(name,col,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.4
 return m
ivory=mat('Printed warm ivory',(.78,.74,.62));blue=mat('Printed blue',(.06,.27,.42));dark=mat('Purchased dark housing',(.025,.038,.047));silver=mat('Metal',(.42,.48,.52),.7);pcb=mat('PCB blue',(.025,.15,.23));gold=mat('Metal contacts',(.64,.37,.08),.65);paper=mat('Household paper',(.93,.90,.78));water=mat('Water surface',(.08,.38,.55),.2);green=mat('Plant leaves',(.14,.3,.08));seedmat=mat('Cress seeds',(.24,.095,.027));floor=mat('Studio ground',(.78,.79,.75));orange=mat('Insulated supply cable',(.62,.23,.045));wiremat=mat('Signal cable',(.055,.065,.075));white=mat('Label white',(.95,.95,.91))
ink=bpy.data.materials.new('Unlit annotation');ink.use_nodes=True;n=ink.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(.018,.03,.038,1);o=n.new('ShaderNodeOutputMaterial');ink.node_tree.links.new(e.outputs[0],o.inputs[0])
def box(name,loc,dim,ma=ivory,bev=.004):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
 if bev:m=o.modifiers.new('Rounded edges','BEVEL');m.width=bev;m.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def rod(name,a,b,r,ma=dark):
 a,b=Vector(a),Vector(b);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=v.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);return o
def sphere(name,p,r,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=r,location=p);o=bpy.context.object;o.name=name;o.data.materials.append(ma);return o
def cable(name,pts,ma=wiremat,r=.002):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for p,co in zip(s.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.scene.collection.objects.link(o);o.data.materials.append(ma);return o
def label(t,p,size=.017,ma=ink,face=True):
 c=bpy.data.curves.new(t,'FONT');c.body=t;c.size=size;c.align_x='CENTER';c.extrude=0
 o=bpy.data.objects.new('Label / '+t,c);bpy.context.scene.collection.objects.link(o);o.location=p;o.data.materials.append(ma)
 if face:o.rotation_euler=bpy.context.scene.camera.rotation_euler
 return o
def overlay(t,x,y,size=.018):
 cam=bpy.context.scene.camera;return label(t,cam.location+cam.rotation_euler.to_quaternion()@Vector((x,y,-.05)),size)
def stl(name,p=(0,0,0),ma=ivory):
 bpy.ops.wm.stl_import(filepath=str(TMP/(name+'.stl')));o=bpy.context.object;o.name='Actual printable mesh / '+name;o.scale=(.001,)*3;o.location=p;o.data.materials.append(ma);return o
def start(name,scale=.7,target=(0,0,.055),loc=(.5,-.8,.75)):
 s=bpy.data.scenes.new(name);bpy.context.window.scene=s;s.world=bpy.data.worlds.new(name+' World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.68,.72,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
 s.render.engine='CYCLES';s.cycles.samples=20;s.cycles.use_denoising=True;s.render.resolution_x=1440;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.clip_start=.001;cam.data.ortho_scale=scale;s.camera=cam
 for pos,power,size in [((.3,-.5,1.2),30,1.2),((-.5,.3,.8),21,1)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 box('Studio surface',(0,0,-.018),(5,5,.025),floor)
 s['geometry_note']='Actual STL meshes where labeled; all other hardware is illustrative and not manufacturing geometry.'
 return s

def refine(name):
 s=bpy.context.scene
 if name=='workbench':
  s.camera.data.ortho_scale*=1.15
  for ob in s.objects:
   if ob.type=='FONT' and ob.data.body=='MAC':ob.hide_render=True
  curves=[ob for ob in s.objects if ob.name.startswith('USB data cable')]
  for i,ob in enumerate(curves):
   ob.data.splines[0].bezier_points[0].co.x=.011+i*.019
 if name=='probe-contact':
  for ob in s.objects:
   if ob.name.startswith(('Illustrative probe PCB','Conductive electrode','Probe screw terminals','Probe wire')):ob.location.z-=.007
 if name in ['light-tool','care-measure','care-park']:
  dx=.038 if name!='care-measure' else .037
  for ob in s.objects:
   if ob.name.startswith(('BH1750 PCB','Sensor package','Header pin')):
    ob.location+=Vector((dx,.036,-.003))
   if name=='light-tool' and ob.name.startswith('Light lead'):
    ob.location+=Vector((dx,.036,-.003))
   if ob.type=='FONT' and ob.data.body=='SENSING FACE UP':ob.location=Vector((0,.044,.055))
  if name=='care-measure':
   for ob in s.objects:
    if ob.name.startswith(('Illustrative wrist','Robot wrist joint','Gripper jaw','Robot arm segment')):ob.location+=Vector((-.041,-.05,0))

def finish(name,title,subtitle):
 refine(name)
 s=bpy.context.scene;scale=s.camera.data.ortho_scale;overlay(title,0,scale*.292,scale*.024);overlay(subtitle,0,-scale*.30,scale*.015)
 s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
def board(x,y,z=0,kind='ESP32'):
 sizes={'ESP32':(.062,.034),'BH1750':(.025,.021),'Relay':(.05,.035),'SHT31':(.028,.02)};w,d=sizes[kind]
 box(kind+' PCB',(x,y,z+.003),(w,d,.003),pcb,.001)
 if kind=='ESP32':
  box('ESP32 RF shield',(x-.006,y,z+.008),(.026,.019,.008),silver,.001);box('USB-C connector',(x+w/2,y,z+.007),(.009,.012,.006),silver,.001)
 elif kind=='Relay':
  box('Relay coil housing',(x,y,z+.014),(.025,.019,.025),blue,.001);box('Relay screw terminal',(x+.021,y,z+.01),(.009,.03,.016),ivory,.001)
 else:box('Sensor package',(x,y,z+.006),(.005,.005,.004),silver,.0005)
 for i in range(6):rod('Header pin',(x-w*.35+i*w*.12,y-d/2,z+.003),(x-w*.35+i*w*.12,y-d/2,z+.012),.0007,gold)
 return (x,y,z)
def laptop(x,y,s=1):
 box('Mac base',(x,y,.012),(.25*s,.17*s,.014),silver);box('Mac display',(x,y+.075*s,.11*s),(.25*s,.013,.18*s),dark)
 box('Display image',(x,y+.066*s,.113*s),(.225*s,.002,.15*s),blue,.001)
 for i in range(5):box('Keyboard',(x,y-.025*s+i*.012*s,.021),(.20*s,.005*s,.001),dark,.001)
def hub(x,y):
 box('Powered USB hub',(x,y,.018),(.15,.048,.03),silver)
 for i in range(7):box('USB socket',(x-.058+i*.019,y-.025,.02),(.013,.003,.008),dark,.001)
def grip(p):
 x,y,z=p;box('Illustrative wrist',(x,y,z+.047),(.055,.05,.04),ivory);rod('Robot wrist joint',(x-.035,y,z+.05),(x+.035,y,z+.05),.022,dark)
 for dx in [-.029,.029]:box('Gripper jaw',(x+dx,y,z),(.012,.027,.065),dark)
 cable('Robot arm segment',[(x,y,z+.065),(x-.08,y+.02,z+.13),(x-.15,y+.09,z+.15)],ivory,.019)
def plants(cx=0,cy=0,z=.022,n=40,w=.13,d=.055,stage=2):
 rng=random.Random(16)
 for i in range(n):
  x=cx+rng.uniform(-w/2,w/2);y=cy+rng.uniform(-d/2,d/2)
  ob=sphere('Seed',(x,y,z),.0017,seedmat);ob.scale=(1.5,1,.6)
  if stage:
   h=rng.uniform(.012,.027) if stage==2 else .008;rod('Shoot',(x,y,z),(x,y,z+h),.00055,green)
   leaf=sphere('Seed leaves',(x,y,z+h),.004,green);leaf.scale=(1.5,.65,.25)
def cress(origin=(0,0,.0235),crop=True,cut=False):
 x,y,z=origin
 obs=[stl('cressmaster-trough',origin),stl('cressmaster-holder',origin,blue)]
 for i in range(4):obs.append(stl('cressmaster-inset',(x+.03*i,y,z),blue))
 if cut:
  cutter=box('Cutaway tool',(x,y-.15,z),(.6,.30,.3),dark,0)
  for ob in obs:
   bpy.context.view_layer.objects.active=ob;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);m=ob.modifiers.new('Illustration front cutaway','BOOLEAN');m.operation='DIFFERENCE';m.object=cutter;bpy.ops.object.modifier_apply(modifier=m.name)
  bpy.data.objects.remove(cutter,do_unlink=True)
 box('Water below growing deck',(x-.0125,y+.016,z-.012),(.165,.032,.009),water,.001)
 box('Household paper',(x,y+.013 if cut else y,z+.002),(.138,.031 if cut else .066,.001),paper,.0004)
 for i in range(4):box('Paper wick',(x-.057+i*.03,y+.015,z-.008),(.007,.02,.022),paper,.0003)
 if crop:plants(x,y+.018 if cut else y,z+.004,n=30,w=.13,d=.025 if cut else .055)
 return obs
# 01 Actual creator meshes with a cutaway, never exported as an STL.
start('01 Wicking planter cutaway',.35,target=(0,0,.035),loc=(.2,-.5,.28));cress(cut=True)
label('PAPER + SEEDLINGS',(0,.025,.075),.008);label('FOUR PAPER WICKS',(0,-.07,.002),.007)
finish('wick-cutaway','WATER INSIDE THE PLANTER','Actual planter meshes cut open for explanation; paper and water are household inputs.')
# 02 complete practical workbench.
start('02 Connected workbench',1.05,target=(0,0,.055),loc=(.4,-.9,1.0));laptop(-.24,.11);hub(.03,.13);board(.24,.11);board(.23,-.075,kind='Relay');board(.04,-.14,kind='BH1750')
box('Two robot USB interfaces',(-.2,-.14,.02),(.12,.065,.035),dark);box('Robot camera',(-.35,-.11,.032),(.05,.04,.05),dark);rod('Camera lens',(-.35,-.137,.032),(-.35,-.145,.032),.014,silver)
for dest in [(-.2,-.14,.04),(-.35,-.11,.05),(.26,.11,.012)]:cable('USB data cable',[(.03,.105,.025),(.07,0,.022),dest],wiremat,.003)
cable('Mac USB uplink',[(-.12,.10,.02),(-.07,.18,.035),(-.01,.14,.025)],wiremat,.003)
box('Hub power adapter',(.30,.24,.018),(.065,.05,.03),dark);cable('Hub adapter lead',[(.30,.22,.02),(.19,.20,.023),(.07,.15,.02)],orange)
box('Separate motor power adapters',(-.29,-.27,.025),(.14,.07,.045),dark)
for t,p in [('MAC',(-.24,.12,.27)),('POWERED HUB',(.03,.14,.08)),('ESP32',(.25,.11,.06)),('MOTOR USB',(-.2,-.14,.075)),('CAMERA',(-.37,-.10,.095)),('LIGHT TOOL',(.04,-.14,.03)),('PROBE RELAY',(.24,-.08,.06)),('MOTOR POWER',(-.29,-.29,.06))]:label(t,p,.016)
finish('workbench','ONE MAC / SEPARATE MOTOR POWER','Illustrative equipment and cable routing; final port types, pinouts and cable lengths need checks.')
# 03 USB closeup.
start('03 ESP32 USB link',.36,target=(0,0,.018));hub(-.065,.055);board(.075,-.055)
cable('USB data lead',[(-.025,.028,.025),(-.04,-.04,.02),(.11,-.09,.013),(.106,-.055,.007)],wiremat,.003)
label('POWERED HUB',(-.07,.07,.055),.009);label('ESP32 USB-C',(.075,-.055,.04),.009)
finish('usb-link','USB CABLE / POWER + SENSOR DATA','Readings return through the hub to the Mac; use a data-capable cable.')
# 04 light paddle with actual printed holder.
start('04 Removable light paddle',.28,target=(0,0,.02));stl('light_paddle',(0,0,.004),blue);board(-.038,0,.014,kind='BH1750')
for i in range(4):cable('Light lead '+str(i),[(-.038+i*.002,-.011,.02),(-.025,-.05-i*.007,.025),(.075,-.05-i*.007,.014)],orange if i==0 else wiremat,.001)
label('SENSING FACE UP',(-.037,.008,.052),.006);label('FOUR FLEXIBLE LEADS',(.032,-.04,.05),.006)
finish('light-tool','ONE REMOVABLE LIGHT PADDLE','Actual holder STL; sensor and harness illustrative. Supply, GND, SDA, SCL; pinout unverified.')
# 05 probe paper contact: show electrodes visibly reaching a clear patch.
start('05 Probe contact test',.32,target=(0,0,.06),loc=(.4,-.7,.45));cress(crop=False);plants(-.03,.014,.028,n=16,w=.045,d=.03)
probe=box('Illustrative probe PCB',(.042,0,.065),(.023,.002,.0625),pcb,.001)
for x in [.036,.048]:box('Conductive electrode',(x,-.0015,.046),(.005,.001,.026),gold,.0004)
box('Probe screw terminals',(.042,0,.099),(.025,.012,.012),ivory,.001)
for i in range(3):cable('Probe wire',[(.034+i*.007,0,.105),(.06+i*.01,.025,.12),(.09+i*.009,.06,.105)],orange if i==0 else wiremat,.0009)
label('SEED-FREE CONTACT PATCH',(.015,-.055,.029),.0065);label('VCC / GND / SIG',(.055,.025,.137),.006)
finish('probe-contact','MOISTURE / GENTLE REPEATABLE CONTACT','Illustrative contact pose; holder depth stop and compliance still need measured fit tests.')
# 06 relay wiring physical parts.
start('06 Probe power electronics',.31,target=(0,0,.015));board(-.073,.035);board(.045,.02,kind='Relay')
for i in range(3):cable('Relay control lead', [(-.06+i*.009,.019,.012),(-.045+i*.005,-.02,.013),(.024+i*.006,.005,.012)],orange if i==1 else wiremat,.001)
box('Probe terminal example',(.065,-.063,.018),(.035,.02,.018),ivory,.002)
cable('Normally open switched supply',[(.067,.018,.018),(.10,-.015,.025),(.075,-.06,.021)],orange,.0015)
label('ESP32',(-.075,.04,.043),.008);label('RELAY MODULE',(.045,.025,.055),.007);label('PROBE POWER',(.06,-.07,.044),.007)
finish('relay-physical','RELAY / SWITCH THE PROBE, NOT A PUMP','Functional layout only. Verify 5V module supply and trigger; contacts switch probe 3.3V.')
# 07 relay contact cutaway (concept, not exact bought module internals).
start('07 Relay contact principle',.28,target=(0,0,.025));box('Opened illustrative relay base',(0,0,.006),(.13,.075,.009),pcb)
for i in range(15):rod('Coil winding',(-.047+i*.002,-.018,.025),(-.047+i*.002,.018,.025),.001,gold)
box('Movable contact',(.008,0,.03),(.055,.009,.003),silver,.001).rotation_euler[1]=-.18
box('Fixed NO contact',(.043,0,.021),(.014,.01,.004),gold,.0005)
rod('COM terminal',(-.01,-.033,.007),(-.01,-.033,.027),.003,silver);rod('NO terminal',(.044,-.033,.007),(.044,-.033,.022),.003,silver)
label('COIL',(-.04,.015,.061),.007);label('OPEN CONTACT GAP',(.025,.012,.066),.007);label('COM',(-.01,-.04,.014),.007);label('NO',(.05,-.04,.014),.007)
finish('relay-cutaway','NORMALLY OPEN / PROBE OFF AT REST','Conceptual internal mechanism, not the exact module. A separate supply powers the coil.')
# 08 full three-plate arrangement, actual meshes, normalized per object then arranged.
def placed(name,x,y,ma=ivory):
 ob=stl(name,(0,0,0),ma);bpy.context.view_layer.update();pts=[ob.matrix_world@Vector(v) for v in ob.bound_box];c=Vector(((min(v.x for v in pts)+max(v.x for v in pts))/2,(min(v.y for v in pts)+max(v.y for v in pts))/2,min(v.z for v in pts)));ob.location+=Vector((x,y,.002))-c;return ob
start('08 Three prepared plates',1.18,target=(0,0,.02),loc=(.3,-.8,1.1))
for x in [-.34,0,.34]:box('K1 Max plate envelope',(x,0,-.002),(.30,.30,.006),dark,.008)
placed('germination_kit_part1',-.34,0);placed('germination_kit_part3',0,.03)
for i in range(3):placed('cressmaster-inset',-.03+i*.025,-.11,blue)
placed('germination_kit_part2',.33,.045,blue);placed('cressmaster-trough',.335,-.10);placed('cressmaster-holder',.335,-.19,blue);placed('cressmaster-inset',.47,-.085,blue)
for t,x in [('1  OUTER TRAY / DONE',-.34),('2  COVER + 3 INSETS',0),('3  INSERT + WICK PARTS',.34)]:label(t,(x,-.245,.022),.015)
finish('print-plates','THE TWO KITS / NINE PRINTED PIECES','Actual meshes arranged for identification; this view is not a slicing or clearance check.')
# 09 sowing growth stages in physical trays.
start('09 Growth observation',.78,target=(0,0,.025));
for i,(name,stage) in enumerate([('DAY 0 / SOW',0),('ROOTS / SHOOTS',1),('GREEN SEED LEAVES',2)]):
 x=(i-1)*.235;cress((x,0,.0235),crop=False);plants(x,0,.028,n=34,stage=stage);label(name,(x,-.092,.04),.012)
finish('growth-stages','WHAT TO LOOK FOR DURING THE NY TRIAL','Illustrative stages, not a growth prediction. Arrival date and conditions determine progress.')
# 10-13 care storyboard with gripper or camera, all physical scenes.
for step in ['inspect','measure','water','park']:
 start('Care / '+step,.55 if step=='water' else .44,target=(0,0,.10 if step=='water' else .085),loc=(.42,-.7,.5));cress()
 if step=='inspect':
  box('Robot camera',(0,.08,.17),(.05,.04,.045),dark);rod('Lens',(0,.058,.165),(0,.04,.155),.013,silver);label('CLEAR VIEW OF CROP',(0,-.075,.06),.01)
 elif step=='measure':
  stl('light_paddle',(.025,0,.09),blue);board(-.012,0,.1,kind='BH1750');grip((.066,.025,.115));label('ONE TOOL AT A TIME',(-.025,-.08,.057),.009)
 elif step=='water':
  grip((-.08,.01,.155));rod('Bottle envelope',(-.08,.006,.151),(-.105,-.028,.105),.021,white);rod('Provisional spout',(-.105,-.028,.105),(-.1,-.005,.065),.006,dark)
  cable('Illustrative small pour',[(-.10,-.005,.062),(-.09,0,.043),(-.085,.006,.026)],water,.0014);label('TEST REFILL ACCESS',(.035,-.075,.07),.009)
 else:
  stl('tool_rest',(.11,.05,.006),blue);stl('light_paddle',(.10,.04,.011),blue);board(.062,.04,.023,kind='BH1750');rod('Upright small bottle',(-.1,.07,.001),(-.1,.07,.065),.021,white);label('RETURN UPRIGHT / LOG OUTCOME',(0,-.09,.055),.008)
 finish('care-'+step,{'inspect':'INSPECT / IDENTIFY THE TRAY','measure':'MEASURE / VALID CONTACT OR LIGHT POSE','water':'CARE / SUPERVISED SMALL POUR','park':'VERIFY / RETURN TO A KNOWN REST'}[step],'Illustrative robot pose; reach, bottle outlet and tool fit are not yet commissioned.')
# 14 sensor bench supporting supplies.
start('14 Electronics assembly supplies',.65,target=(0,0,.02));
for x,y,k in [(-.20,.1,'ESP32'),(-.06,.1,'Relay'),(.09,.1,'BH1750'),(.21,.1,'SHT31')]:board(x,y,kind=k);label(k,(x,y,.05),.011)
box('Breadboard',(-.16,-.06,.013),(.12,.065,.024),paper)
for ix in range(20):
 for iy in range(6):box('Breadboard hole',(-.21+ix*.005,-.078+iy*.006,.026),(.002,.002,.001),dark,0)
box('Perfboard',(.06,-.055,.005),(.10,.07,.004),gold,.001)
for ix in range(16):
 for iy in range(10):rod('Perfboard plated hole',(.015+ix*.006,-.08+iy*.006,.007),(.015+ix*.006,-.08+iy*.006,.008),.001,silver)
for i in range(4):cable('Flexible cable',[(.17,-.09+i*.01,.003),(.25,-.04+i*.01,.006),(.22,.025+i*.01,.003)],orange if i==0 else wiremat,.0015)
label('BREADBOARD',(-.16,-.105,.023),.011);label('PERFBOARD',(.06,-.105,.023),.011);label('FLEXIBLE WIRE',(.22,-.1,.04),.010)
finish('electronics-parts','BUILD THE DRY SENSOR BENCH FIRST','Representative parts, not exact purchased geometry. Optional air sensor stays off the arm.')
# 15 recipe / evidence represented on an actual laptop; no physical extra computer implied.
start('15 Software evidence workstation',.60,target=(0,.035,.07));laptop(0,.03,1.3)
for i in range(3):box('Recorded image tile',(-.09+i*.09,.113,.195),(.073,.003,.045),ivory,.002)
for i in range(4):box('Evidence row',(0,.111,.10+i*.014),(.26,.003,.005),silver,.001)
box('Notebook',(.22,-.09,.01),(.10,.13,.015),ivory)
label('PHOTOS / READINGS / ACTION RECORDS',(0,.05,.29),.011);label('LOCAL REVIEW',(.21,-.08,.045),.009)
finish('evidence-workstation','SOFTWARE / A REVIEWABLE CARE RECORD','Illustrative interface concept. The robot logger, Jev/Astra integrations and recovery UI are not built.')
# 16 dry packing, keep seed/local supplies distinct in caption rather than customs promise.
start('16 Dry travel packing',.65,target=(0,0,.045));box('Open carry-on case bottom',(0,0,.006),(.48,.33,.025),dark,.015)
for x in [-.24,.24]:box('Case side',(x,0,.035),(.015,.33,.065),dark)
for y in [-.165,.165]:box('Case side',(0,y,.035),(.48,.015,.065),dark)
placed('germination_kit_part1',-.09,.015);cress((.11,-.07,.03),crop=False)
# Remove water/paper from this clean dry packing scene.
for ob in list(bpy.context.scene.objects):
 if ob.name.startswith(('Water below','Household paper','Paper wick')):bpy.data.objects.remove(ob,do_unlink=True)
board(.16,.1,.025);rod('Empty bottle',(.18,.015,.03),(.18,.015,.095),.021,white)
finish('dry-packing','CLEAN, DRY PARTS / EMPTY BOTTLE','No live crop, used medium or irrigation water. This is a packing illustration, not customs clearance.')
# Functional test-first alternative: actual seven-part packing, not sent automatically.
start('17 Both kits first',.60,target=(0,0,.02),loc=(.15,-.35,.65))
box('K1 Max bed envelope',(0,0,-.002),(.30,.30,.006),dark,.003)
def place_rotated(name,x,y,angle=0,ma=ivory):
 ob=stl(name,(0,0,0),ma);ob.rotation_euler.z=angle;bpy.context.view_layer.update()
 pts=[ob.matrix_world@Vector(v) for v in ob.bound_box]
 center=Vector(((min(v.x for v in pts)+max(v.x for v in pts))/2,(min(v.y for v in pts)+max(v.y for v in pts))/2,min(v.z for v in pts)))
 ob.location+=Vector((x,y,.002))-center
 return ob
place_rotated('germination_kit_part2',.049,.044,ma=blue)
place_rotated('cressmaster-trough',-.096,.0515,math.pi/2)
place_rotated('cressmaster-holder',-.05751,-.10,ma=blue)
for y in [-.13,-.11,-.09,-.07]:place_rotated('cressmaster-inset',.08,y,math.pi/2,blue)
finish('both-kits-first','BOTH KITS FIRST / SEVEN PARTS','Square insert + complete cress planter. Sliced: 10h06m / 274.84 g. Printed cover deferred.')

# One file with named editable scenes and packed render-independent geometry.
unused=bpy.data.scenes.get('Unused')
if unused:bpy.data.scenes.remove(unused)
bpy.context.window.scene=bpy.data.scenes['01 Wicking planter cutaway']
for s in bpy.data.scenes:s.render.filepath='//../assets/blender/'+Path(s.render.filepath).name
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'handbook/downloads/farm-visual-atlas.blend'),compress=True)
print('ALL SCENES SAVED',flush=True)
