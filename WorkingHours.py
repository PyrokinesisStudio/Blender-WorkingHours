import bpy, os, time, datetime, configparser
from bpy.app.handlers import persistent

############
# VARIABLE #
############

bl_info = {
	"name" : "Working Hours",
	"author" : "Saidenka",
	"version" : (0,1),
	"blender" : (2, 7),
	"location" : "Upper right",
	"description" : "Record working hours of Blender",
	"warning" : "",
	"wiki_url" : "http://github.com/saidenka/Blender-WorkingHours",
	"tracker_url" : "http://github.com/saidenka/Blender-WorkingHours/issues",
	"category" : "System"
}

MODE_NAMES_AND_ICONS = (
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
	('PARTICLE', 'PARTICLEMODE'))

#############
# FUNCTIONS #
#############

def ResetPreferences():
	pref = bpy.context.user_preferences.addons[__name__].preferences
	value_names = ['ALL', 'OBJECT', 'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_TEXT', 'EDIT_ARMATURE',
		'EDIT_METABALL', 'EDIT_LATTICE', 'POSE', 'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE', 'PARTICLE']
	for value_name in value_names:
		pref.__setattr__(value_name, 0.0)
	pref.pre_time = GetTime()

def GetIniPath():
	ini_name = os.path.splitext(bpy.path.basename(__file__))[0] + ".ini"
	base_dir = os.path.dirname(__file__)
	return os.path.join(base_dir, ini_name)

def GetConfig():
	config = configparser.ConfigParser()
	config.read(GetIniPath())
	return config

def GetBlendPathSection():
	if (bpy.data.filepath == ""):
		return 'NoFile'
	return bpy.data.filepath

def GetTime():
	return time.perf_counter()

def GetDayString():
	reset_hour = bpy.context.user_preferences.addons[__name__].preferences.reset_hour
	date = datetime.date.today() + datetime.timedelta(hours=reset_hour)
	return date.strftime('%Y-%m-%d')

@persistent
def load_handler(scene):
	ResetPreferences()

def GetTimeString(raw_sec, is_minus=False):
	sec = int(raw_sec)
	if (sec == 0):
		return "..."
	minus = ""
	if (is_minus):
		minus = "-"
	if (60 <= raw_sec):
		sec = int( raw_sec % 60 )
		min = int( raw_sec / 60 )
		if (60 <= min):
			hour = int( raw_sec / 60 / 60 )
			min = int( (raw_sec / 60) % 60 )
			sec = int( raw_sec % 60 )
			return minus + str(hour) + "h" + str(min) + "m" + str(sec) + "s"
		sec = int( raw_sec % 60 )
		return minus + str(min) + "m" + str(sec) + "s"
	return minus + str(sec) + "s"

###############
# PREFERENCES #
###############

class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	ignore_time_interval = bpy.props.FloatProperty(name="AFK Interval (Second)", default=60, min=1, max=9999, soft_min=1, soft_max=9999)
	reset_hour = bpy.props.IntProperty(name="Day Reset Hour", default=4, min=0, max=24, soft_min=0, soft_max=24)
	
	show_toggle_buttons = bpy.props.BoolProperty(name="Expand Buttons", default=False)
	show_day_time = bpy.props.BoolProperty(name="Show Day Time", default=True)
	show_this_work_time = bpy.props.BoolProperty(name="Show New Time", default=True)
	show_this_file_work_time = bpy.props.BoolProperty(name="Show File Time", default=True)
	show_all_work_time = bpy.props.BoolProperty(name="Show All Time", default=True)
	
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
		self.layout.prop(self, 'show_toggle_buttons')
		row = self.layout.row()
		for value_name in ['show_this_work_time', 'show_this_file_work_time', 'show_all_work_time']:
			row.prop(self, value_name)
		row = self.layout.row()
		row.prop(self, 'ignore_time_interval')
		row.prop(self, 'reset_hour')

############
# OPERATOR #
############

class DeleteWorkingHoursData(bpy.types.Operator):
	bl_idname = 'wm.delete_working_hours_data'
	bl_label = "Delete WorkingHours Savedata"
	bl_description = "Delete WorkingHours Savedata?"
	bl_options = {'REGISTER'}
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
	def execute(self, context):
		os.remove(GetIniPath())
		ResetPreferences()
		return {'FINISHED'}

########
# MENU #
########

class ThisWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_this_work_time'
	bl_label = ""
	
	def draw(self, context):
		global MODE_NAMES_AND_ICONS
		pref = context.user_preferences.addons[__name__].preferences
		self.layout.label(GetTimeString(pref.ALL), icon='TIME')
		self.layout.separator()
		for mode, icon in MODE_NAMES_AND_ICONS:
			text = GetTimeString(pref.__getattribute__(mode))
			self.layout.label(text, icon=icon)
		self.layout.separator()
		self.layout.label(GetTimeString(GetTime() - pref.ALL, is_minus=True), icon='CANCEL')

class DayTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_day_time'
	bl_label = ""
	
	def draw(self, context):
		global MODE_NAMES_AND_ICONS
		config = GetConfig()
		day_str = GetDayString()
		text = GetTimeString(float(config.get(day_str, 'all', fallback='0.0')))
		self.layout.label(text, icon='TIME')
		self.layout.separator()
		for mode, icon in MODE_NAMES_AND_ICONS:
			text = GetTimeString(float(config.get(day_str, mode, fallback='0.0')))
			self.layout.label(text, icon=icon)

class ThisFileWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_this_file_work_time'
	bl_label = ""
	
	def draw(self, context):
		global MODE_NAMES_AND_ICONS
		config = GetConfig()
		blend_path = GetBlendPathSection()
		text = GetTimeString(float(config.get(blend_path, 'all', fallback='0.0')))
		self.layout.label(text, icon='TIME')
		self.layout.separator()
		for mode, icon in MODE_NAMES_AND_ICONS:
			text = GetTimeString(float(config.get(blend_path, mode, fallback='0.0')))
			self.layout.label(text, icon=icon)

class AllWorkTimeMenu(bpy.types.Menu):
	bl_idname = 'INFO_HT_header_all_work_time'
	bl_label = ""
	
	def draw(self, context):
		config = GetConfig()
		text = GetTimeString(float(config.get('ALL', 'all', fallback='0.0')))
		self.layout.label(text, icon='TIME')
		self.layout.separator()
		for mode, icon in MODE_NAMES_AND_ICONS:
			text = GetTimeString(float(config.get('ALL', mode, fallback='0.0')))
			self.layout.label(text, icon=icon)

##########
# LAYOUT #
##########

def header_func(self, context):
	pref = context.user_preferences.addons[__name__].preferences
	config = GetConfig()
	blend_path = GetBlendPathSection()
	day_str = GetDayString()
	
	if (blend_path not in config):
		config[blend_path] = {}
	if ('ALL' not in config):
		config['ALL'] = {}
	if (day_str not in config):
		config[day_str] = {}
	
	time_diff = GetTime() - pref.pre_time
	if (time_diff < 0.0):
		time_diff, pref.ALL = 0.0, 0.0
	
	all_time = float(config.get('ALL', 'all', fallback='0.0'))
	day_time = float(config.get(day_str, 'all', fallback='0.0'))
	this_file_time = float(config.get(blend_path, 'all', fallback='0.0'))
	if (time_diff < pref.ignore_time_interval):
		pref.ALL += time_diff
		day_time += time_diff
		this_file_time += time_diff
		all_time += time_diff
		
		time_mode = pref.__getattribute__(context.mode)
		pref.__setattr__(context.mode, time_mode + time_diff)
		
		time_mode = float(config.get(day_str, context.mode, fallback='0.0'))
		config[day_str][context.mode] = str(time_mode + time_diff)
		
		time_mode = float(config.get(blend_path, context.mode, fallback='0.0'))
		config[blend_path][context.mode] = str(time_mode + time_diff)
		
		time_mode = float(config.get('ALL', context.mode, fallback='0.0'))
		config['ALL'][context.mode] = str(time_mode + time_diff)
	pref.pre_time = GetTime()
	
	row = self.layout.row(align=True)
	if (pref.show_this_work_time):
		row.menu(ThisWorkTimeMenu.bl_idname, icon='TIME', text="  New " + GetTimeString(pref.ALL))
	if (pref.show_day_time):
		row.menu(DayTimeMenu.bl_idname, icon='FILE_BLEND', text="  Day " + GetTimeString(day_time))
	if (pref.show_this_file_work_time):
		row.menu(ThisFileWorkTimeMenu.bl_idname, icon='FILE_BLEND', text="  File " + GetTimeString(this_file_time))
	if (pref.show_all_work_time):
		row.menu(AllWorkTimeMenu.bl_idname, icon='BLENDER', text="  All " + GetTimeString(all_time))
	
	row = self.layout.row(align=True)
	path = 'user_preferences.addons["' + __name__ + '"].preferences.'
	if (pref.show_toggle_buttons):
		for value_name in ['show_this_work_time', 'show_day_time', 'show_this_file_work_time', 'show_all_work_time']:
			if (pref.__getattribute__(value_name)):
				row.operator('wm.context_toggle', icon='X', text="").data_path = path + value_name
			else:
				row.operator('wm.context_toggle', icon='RESTRICT_VIEW_OFF', text="").data_path = path + value_name
		row.operator(DeleteWorkingHoursData.bl_idname, icon='CANCEL', text="")
		
		row.operator('wm.context_toggle', icon='TRIA_LEFT', text="").data_path = path + 'show_toggle_buttons'
	else:
		row.operator('wm.context_toggle', icon='ARROW_LEFTRIGHT', text="").data_path = path + 'show_toggle_buttons'
	
	config['ALL']['all'] = str(all_time)
	config[day_str]['all'] = str(day_time)
	config[blend_path]['all'] = str(this_file_time)
	with open(GetIniPath(), 'w') as file:
		config.write(file)

#############
# REGISTERS #
#############

def register():
	bpy.utils.register_module(__name__)
	ResetPreferences()
	bpy.types.INFO_HT_header.append(header_func)
	bpy.app.handlers.load_post.append(load_handler)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_HT_header.remove(header_func)
	bpy.app.handlers.load_post.remove(load_handler)

if __name__ == '__main__':
	register()
