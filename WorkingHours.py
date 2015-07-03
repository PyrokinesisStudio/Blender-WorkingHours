import bpy, os, time, configparser
from bpy.app.handlers import persistent

bl_info = {
	"name" : "Working Hours",
	"author" : "Saidenka",
	"version" : (0,1),
	"blender" : (2, 7),
	"location" : "Upper right",
	"description" : "Record working hours of Blender",
	"warning" : "",
	"wiki_url" : "",
	"tracker_url" : "",
	"category" : "System"
}

def GetIniPath():
	ini_name = os.path.splitext(bpy.path.basename(__file__))[0] + ".ini"
	base_dir = os.path.dirname(__file__)
	return os.path.join(base_dir, ini_name)

def GetConfig():
	config = configparser.ConfigParser()
	config.read(GetIniPath())
	return config

@persistent
def load_handler(scene):
	pref = bpy.context.user_preferences.addons[__name__].preferences
	for value_name in ['pre_time', 'ALL', 'OBJECT', 'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_TEXT', 'EDIT_ARMATURE', 'EDIT_METABALL', 'EDIT_LATTICE', 'POSE', 'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE', 'PARTICLE']:
		pref.__setattr__(value_name, 0.0)

class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	ignore_time_interval = bpy.props.FloatProperty(name="Ignore Time Interval (Second)", default=60, min=1, max=9999, soft_min=1, soft_max=9999, step=3, precision=2)
	
	pre_time = bpy.props.FloatProperty(default=0.0)
	ALL = bpy.props.FloatProperty(default=0.0)
	
	OBJECT = bpy.props.FloatProperty(default=0.0)
	EDIT_MESH = bpy.props.FloatProperty(default=0.0)
	EDIT_CURVE = bpy.props.FloatProperty(default=0.0)
	EDIT_SURFACE = bpy.props.FloatProperty(default=0.0)
	EDIT_TEXT = bpy.props.FloatProperty(default=0.0)
	EDIT_ARMATURE = bpy.props.FloatProperty(default=0.0)
	EDIT_METABALL = bpy.props.FloatProperty(default=0.0)
	EDIT_LATTICE = bpy.props.FloatProperty(default=0.0)
	POSE = bpy.props.FloatProperty(default=0.0)
	SCULPT = bpy.props.FloatProperty(default=0.0)
	PAINT_WEIGHT = bpy.props.FloatProperty(default=0.0)
	PAINT_VERTEX = bpy.props.FloatProperty(default=0.0)
	PAINT_TEXTURE = bpy.props.FloatProperty(default=0.0)
	PARTICLE = bpy.props.FloatProperty(default=0.0)
	
	def draw(self, context):
		self.layout.prop(self, 'ignore_time_interval')

def GetTimeString(raw_sec, is_minus=False):
	sec = round(raw_sec)
	if (sec == 0):
		return "..."
	minus = ""
	if (is_minus):
		minus = "-"
	if (60 <= sec):
		min = int(sec / 60)
		if (60 <= min):
			hour = int(sec / 60 / 60)
			min = int((sec / 60) % 60)
			sec = int(sec % 60)
			return minus + str(hour) + "h" + str(min) + "m" + str(sec) + "s"
		sec = int(sec % 60)
		return minus + str(min) + "m" + str(sec) + "s"
	return minus + str(sec) + "s"

class ThisWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_this_work_time'
	bl_label = "ThisWork"
	
	def draw(self, context):
		pref = context.user_preferences.addons[__name__].preferences
		self.layout.label(GetTimeString(pref.ALL), icon='TIME')
		self.layout.separator()
		self.layout.label(GetTimeString(pref.OBJECT), icon='OBJECT_DATA')
		self.layout.label(GetTimeString(pref.EDIT_MESH), icon='MESH_DATA')
		self.layout.label(GetTimeString(pref.EDIT_CURVE), icon='CURVE_DATA')
		self.layout.label(GetTimeString(pref.EDIT_SURFACE), icon='SURFACE_DATA')
		self.layout.label(GetTimeString(pref.EDIT_TEXT), icon='FONT_DATA')
		self.layout.label(GetTimeString(pref.EDIT_ARMATURE), icon='ARMATURE_DATA')
		self.layout.label(GetTimeString(pref.EDIT_METABALL), icon='META_DATA')
		self.layout.label(GetTimeString(pref.EDIT_LATTICE), icon='LATTICE_DATA')
		self.layout.label(GetTimeString(pref.POSE), icon='POSE_HLT')
		self.layout.label(GetTimeString(pref.SCULPT), icon='SCULPTMODE_HLT')
		self.layout.label(GetTimeString(pref.PAINT_WEIGHT), icon='WPAINT_HLT')
		self.layout.label(GetTimeString(pref.PAINT_VERTEX), icon='VPAINT_HLT')
		self.layout.label(GetTimeString(pref.PAINT_TEXTURE), icon='TPAINT_HLT')
		self.layout.label(GetTimeString(pref.PARTICLE), icon='PARTICLEMODE')
		self.layout.separator()
		self.layout.label(GetTimeString(time.clock() - pref.ALL, is_minus=True), icon='CANCEL')

class ThisFileWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_this_file_work_time'
	bl_label = "ThisFileWork"
	
	def draw(self, context):
		blend_path = bpy.data.filepath
		if (blend_path == ""):
			blend_path = 'NoFile'
		mode_names = (
			('OBJECT', 'OBJECT_DATA'),
			('EDIT_MESH', 'MESH_DATA'),
			('EDIT_CURVE', 'CURVE_DATA'),
			('EDIT_SURFACE', 'SURFACE_DATA'),
			('EDIT_TEXT', 'FONT_DATA'),
			('EDIT_ARMATURE', 'ARMATURE_DATA'),
			('EDIT_METABALL', 'META_DATA'),
			('EDIT_LATTICE', 'LATTICE_DATA'),
			('POSE', 'POSE_HLT'),
			('SCULPT', 'SCULPTMODE_HLT'),
			('PAINT_WEIGHT', 'WPAINT_HLT'),
			('PAINT_VERTEX', 'VPAINT_HLT'),
			('PAINT_TEXTURE', 'TPAINT_HLT'),
			('PARTICLE', 'PARTICLEMODE'),
			)
		config = GetConfig()
		text = GetTimeString(float(config.get(blend_path, 'all', fallback='0.0')))
		self.layout.label(text, icon='TIME')
		self.layout.separator()
		for mode, icon in mode_names:
			text = GetTimeString(float(config.get(blend_path, mode, fallback='0.0')))
			self.layout.label(text, icon=icon)

class AllWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_all_work_time'
	bl_label = "AllWork"
	
	def draw(self, context):
		mode_names = (
			('OBJECT', 'OBJECT_DATA'),
			('EDIT_MESH', 'MESH_DATA'),
			('EDIT_CURVE', 'CURVE_DATA'),
			('EDIT_SURFACE', 'SURFACE_DATA'),
			('EDIT_TEXT', 'FONT_DATA'),
			('EDIT_ARMATURE', 'ARMATURE_DATA'),
			('EDIT_METABALL', 'META_DATA'),
			('EDIT_LATTICE', 'LATTICE_DATA'),
			('POSE', 'POSE_HLT'),
			('SCULPT', 'SCULPTMODE_HLT'),
			('PAINT_WEIGHT', 'WPAINT_HLT'),
			('PAINT_VERTEX', 'VPAINT_HLT'),
			('PAINT_TEXTURE', 'TPAINT_HLT'),
			('PARTICLE', 'PARTICLEMODE'),
			)
		config = GetConfig()
		text = GetTimeString(float(config.get('ALL', 'all', fallback='0.0')))
		self.layout.label(text, icon='TIME')
		self.layout.separator()
		for mode, icon in mode_names:
			text = GetTimeString(float(config.get('ALL', mode, fallback='0.0')))
			self.layout.label(text, icon=icon)

def header_func(self, context):
	pref = context.user_preferences.addons[__name__].preferences
	config = GetConfig()
	
	blend_path = bpy.data.filepath
	if (blend_path == ""):
		blend_path = 'NoFile'
	
	if (blend_path not in config):
		config[blend_path] = {}
	if ('ALL' not in config):
		config['ALL'] = {}
	
	time_diff = time.clock() - pref.pre_time
	if (time_diff < 0.0):
		time_diff = 0.0
		pref.ALL = 0.0
	
	all_time = float(config.get('ALL', 'all', fallback='0.0'))
	this_file_time = float(config.get(blend_path, 'all', fallback='0.0'))
	if (time_diff < pref.ignore_time_interval):
		pref.ALL += time_diff
		this_file_time += time_diff
		all_time += time_diff
		
		time_mode = pref.__getattribute__(context.mode)
		pref.__setattr__(context.mode, time_mode + time_diff)
		
		time_mode = float(config.get(blend_path, context.mode, fallback='0.0'))
		config[blend_path][context.mode] = str(time_mode + time_diff)
		
		time_mode = float(config.get('ALL', context.mode, fallback='0.0'))
		config['ALL'][context.mode] = str(time_mode + time_diff)
	pref.pre_time = time.clock()
	
	row = self.layout.row(align=True)
	row.menu(ThisWorkTimeMenu.bl_idname, icon='TIME', text="  ThisWork " + GetTimeString(pref.ALL))
	row.menu(ThisFileWorkTimeMenu.bl_idname, icon='FILE_BLEND', text="  ThisFile " + GetTimeString(this_file_time))
	row.menu(AllWorkTimeMenu.bl_idname, icon='BLENDER', text="  AllWork " + GetTimeString(all_time))
	
	config['ALL']['all'] = str(all_time)
	config[blend_path]['all'] = str(this_file_time)
	with open(GetIniPath(), 'w') as file:
		config.write(file)

def register():
	bpy.utils.register_module(__name__)
	pref = bpy.context.user_preferences.addons[__name__].preferences
	for value_name in ['pre_time', 'ALL', 'OBJECT', 'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_TEXT', 'EDIT_ARMATURE', 'EDIT_METABALL', 'EDIT_LATTICE', 'POSE', 'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE', 'PARTICLE']:
		pref.__setattr__(value_name, 0.0)
	bpy.types.INFO_HT_header.append(header_func)
	bpy.app.handlers.load_post.append(load_handler)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_HT_header.remove(header_func)
	bpy.app.handlers.load_post.remove(load_handler)

if __name__ == '__main__':
	register()