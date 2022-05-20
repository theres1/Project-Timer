 
 #  ***** BEGIN GPL LICENSE BLOCK *****
 #
 #  This program is free software: you can redistribute it and/or modify
 #  it under the terms of the GNU General Public License as published by
 #  the Free Software Foundation, either version 3 of the License, or
 #  (at your option) any later version.
 #
 #  This program is distributed in the hope that it will be useful,
 #  but WITHOUT ANY WARRANTY; without even the implied warranty of
 #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #  GNU General Public License for more details.
 #
 #  You should have received a copy of the GNU General Public License
 #  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 #
 #  The Original Code is Copyright (C) 2013 by Marcin Zielinski
 #  All rights reserved.
 #
 #  Contact:      martin.zielinsky@gmail.com
 #  Information:  http://<domain>.<ext>	###
 #
 #  The Original Code is: all of this file.
 #
 #  Contributor(s): none yet.
 #
 #  ***** END GPL LICENSE BLOCK *****

 
bl_info = {
    "name": "Project Timer",
    "author": "Martin Zielinski",
    "version": (1, 4, 2),
    "blender": (3, 0, 0),
    "location": "Info",
    "description": "Show time spent on project",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Interface"}

# Is this script helpful? Please donate
# BTC 19pXNYUaktXE2MXK37gVEZkrVjL3TwZhF

import bpy
import time
from bpy.app.handlers import persistent 

class ProjectTimerReset(bpy.types.Operator):
    bl_idname = "poject_timer.reset"
    bl_label = "Reset Project Timer"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        bpy.projectTime = 0
        return {'FINISHED'}

class ProjectTimerPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator("poject_timer.reset")
        
            
bpy.types.Scene.projectTime = bpy.props.IntProperty(
            name = "Project Time",
            description='All time spent on project',
            default = 0)

def draw_counter(self, context):
    projectTimerUpdate(context.scene)
        
    layout = self.layout
    region = context.region    

    if region.alignment == 'RIGHT':
        seconds = bpy.projectTime
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        layout.label(text=str(h)+':'+format(m, '02d')+':'+format(s, '02d'))

def projectTimerUpdate(scene):
    if not hasattr(bpy, 'projectTimestamp'): #first open
        bpy.projectTime = scene.projectTime
        bpy.projectTimestamp = int(time.time())
        print('Project Time: ', bpy.projectTime)
        print('Project Timestamp: ', bpy.projectTimestamp)
    delta = int(time.time()) - bpy.projectTimestamp
    if delta < 30:
        bpy.projectTime += delta
    bpy.projectTimestamp = int(time.time())

@persistent 
def projectTimerSave(scene):
    projectTimerUpdate(scene)
    bpy.context.scene.projectTime = bpy.projectTime
    print('Project Time saved', bpy.projectTime)

@persistent    
def projectTimerLoad(scene):
    bpy.projectTime = bpy.context.scene.projectTime
    bpy.projectTimestamp = int(time.time())
    print('Project Time loaded', bpy.projectTime)

# Registration

def register():
    bpy.app.handlers.load_post.append(projectTimerLoad)
    bpy.app.handlers.save_pre.append(projectTimerSave)
    bpy.utils.register_class(ProjectTimerReset)
    bpy.utils.register_class(ProjectTimerPreferences)
    bpy.types.TOPBAR_HT_upper_bar.append(draw_counter)


def unregister():
    bpy.app.handlers.load_post.remove(projectTimerLoad)
    bpy.app.handlers.save_pre.remove(projectTimerSave)
    bpy.utils.unregister_class(ProjectTimerReset)
    bpy.utils.unregister_class(ProjectTimerPreferences)
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_counter)
    

if __name__ == "__main__":
    register()