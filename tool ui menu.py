# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Frankies Animation Tool",
    "author": "Frankie Hobbins",
    "version": (0, 1),
    "blender": (2, 76, 0),
    "description": "Misc Animation tools",
    "category": "Animation",
    }


import bpy
from bpy.props import *

obj = bpy.context.object                    #active object
scn = bpy.context.scene                     #current scene

if obj.animation_data != None:
    action = obj.animation_data.action      #current action

########################
####### FUNCTIONS ######
########################

def whatsMyAction():
    i = 0
    for action in bpy.data.actions:
        if action.name == bpy.context.object.animation_data.action.name:
            actionindex = i
        i += 1
    return(actionindex)

#######################
###### OPERATORS ######
#######################

class KeyFrameAllActions(bpy.types.Operator):
    """Add a keyframe for Selcted bone on all actions """
    bl_idname = "bone.keyframeallactions"
    bl_label = "Unused"

    def execute(self, context):
        for selbone in bpy.context.selected_pose_bones:
            bone_path = '"' + selbone.name + '"'
            #for fc in action.fcurves:
            for a in bpy.data.actions:
                for fc in a.fcurves:
                    if bone_path not in fc.data_path:
                        continue                    
                    while len(fc.keyframe_points):
                        fc.keyframe_points.remove(fc.keyframe_points[0])
        return{'FINISHED'}

class RemoveKeyFrames(bpy.types.Operator):
    """ Remove selected bone keyframes from all actions """
    bl_idname = "bone.removekeyframes"
    bl_label = "Unused"

    def execute(self, context):
        for selbone in bpy.context.selected_pose_bones:
            bone_path = '"' + selbone.name + '"'
            for a in bpy.data.actions:
                for fc in a.fcurves:
                    if bone_path not in fc.data_path:
                        continue
                    while len(fc.keyframe_points):
                        fc.keyframe_points.remove(fc.keyframe_points[0])
        return{'FINISHED'}

class RemoveKeyFramesApartFromOne(bpy.types.Operator):
    """Remove all but a single non specific keyframe on all actions as long as run or idle isn't in the name """
    bl_idname = "bone.removekeyframesapartfromone"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            if "run" not in a.name:
                if "idle" not in a.name:
                    for fc in a.fcurves:
                        while len(fc.keyframe_points):
                            fc.keyframe_points.remove(fc.keyframe_points[0])
        return{'FINISHED'}

class ActionstOnNlaStrips(bpy.types.Operator):
    """Clear NLA stash and then move Actions to NLA area(handy for exporting specific anims to fbx)"""
    bl_idname = "bone.actionstonnlastrips"
    bl_label = "Unused"

    def execute(self, context):
        for nlatrack in bpy.context.object.animation_data.nla_tracks:
            bpy.context.object.animation_data.nla_tracks.remove(nlatrack)

        for action in bpy.data.actions:
            print(action)
            bpy.context.object.animation_data.nla_tracks.new()
            bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].name = action.name
            bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].strips.new(action.name,0,action)

        #mute
        for nlatrack in bpy.context.object.animation_data.nla_tracks:
            nlatrack.mute=True

        return{'FINISHED'}

class UnmuteNlaStrips(bpy.types.Operator):
    """Unmute all NLA strips(handy to specify which anims to export on fbx)"""
    bl_idname = "bone.unmutenlastrips"
    bl_label = "Unused"

    def execute(self, context):
        for nlatrack in bpy.context.object.animation_data.nla_tracks:
            nlatrack.mute=False
        return{'FINISHED'}

class MuteNlaStrips(bpy.types.Operator):
    """Mute all NLA strips(handy to specify which anims to export on fbx)"""
    bl_idname = "bone.mutenlastrips"
    bl_label = "Unused"

    def execute(self, context):
        for nlatrack in bpy.context.object.animation_data.nla_tracks:
            nlatrack.mute=True
        return{'FINISHED'}

class NextAction(bpy.types.Operator):
    """Add Fake users to all actions to stop them getting deleted on save"""
    bl_idname = "bone.nextaction"
    bl_label = "Unused"

    def execute(self, context):
        if whatsMyAction() < len(bpy.data.actions)-1:
            bpy.context.object.animation_data.action = bpy.data.actions[whatsMyAction()+1]
        return{'FINISHED'}

class PrevAction(bpy.types.Operator):
    """Add Fake users to all actions to stop them getting deleted on save"""
    bl_idname = "bone.prevaction"
    bl_label = "Unused"

    def execute(self, context):           
        if whatsMyAction() > 0:
            bpy.context.object.animation_data.action = bpy.data.actions[whatsMyAction()-1]
        return{'FINISHED'}

class AddFakeUsers(bpy.types.Operator):
    """Add Fake users to all actions to stop them getting deleted on save"""
    bl_idname = "bone.addfakeusers"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            a.use_fake_user=True
        return{'FINISHED'}

class RemoveFakeUsers(bpy.types.Operator):
    """Remove Fake users from all actions to help them getting removed on save"""
    bl_idname = "bone.removefakeusers"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            a.user_clear()
            a.use_fake_user=False
        return{'FINISHED'}

class CleanAnimData(bpy.types.Operator):
    """Go though all objects and remove anim data from anything that isn't an Armature so you dont have meshes keeping actions from getting deleted"""
    bl_idname = "bone.cleananimdata"
    bl_label = "Unused"

    def execute(self, context):
        for object in bpy.data.objects:
            if object.type != 'ARMATURE':
                if object.animation_data != None:
                    object.animation_data.action = None
        return{'FINISHED'}

class SmartKeyframeFix(bpy.types.Operator):
    """Duplicate last keyframe and move to the first"""
    bl_idname = "bone.smartkeyframefix"
    bl_label = "Unused"

    def execute(self, context):
        if bpy.context.selected_pose_bones != None:  
            if bpy.context.selected_pose_bones.count != 0:    
                for selbone in bpy.context.selected_pose_bones:
                    for f in bpy.data.actions[action.name].fcurves:
                        b = (str(f.data_path))
                        if ("\""+selbone.name+"\"") in b:
                            for k in f.keyframe_points:
                                if bpy.context.scene.frame_current < (0.5*bpy.context.scene.frame_end):
                                    print (0.5*bpy.context.scene.frame_end)
                                    if k.co[0] == bpy.context.scene.frame_end:
                                        k.co[1]= f.evaluate(0)
                                else:
                                    print("start to end")
                                    if k.co[0] == 0:
                                        k.co[1]= f.evaluate(bpy.context.scene.frame_end)
                            f.update()
        return{'FINISHED'}

class KeyframeLastToFirst(bpy.types.Operator):
    """Duplicate last keyframe and move to the first"""
    bl_idname = "bone.keyframelasttofirst"
    bl_label = "Unused"

    def execute(self, context):
        if bpy.context.selected_pose_bones != None:  
            if bpy.context.selected_pose_bones.count != 0:    
                for selbone in bpy.context.selected_pose_bones:
                    for f in bpy.data.actions[action.name].fcurves:
                        b = (str(f.data_path))
                        if ("\""+selbone.name+"\"") in b:
                            for k in f.keyframe_points:
                                if k.co[0] == bpy.context.scene.frame_end:
                                    k.co[1]= f.evaluate(0)
                            f.update()
        return{'FINISHED'}        

class KeyframeFirstToLast(bpy.types.Operator):
    """Duplicate first keyframe and move to the last """
    bl_idname = "bone.keyframefirsttolast"
    bl_label = "Unused"

    def execute(self, context):
        if bpy.context.selected_pose_bones != None:  
            if bpy.context.selected_pose_bones.count != 0:    
                for selbone in bpy.context.selected_pose_bones:
                    for f in bpy.data.actions[action.name].fcurves:
                        b = (str(f.data_path))
                        if ("\""+selbone.name+"\"") in b:
                            for k in f.keyframe_points:
                                if k.co[0] == 0:
                                    k.co[1]= f.evaluate(bpy.context.scene.frame_end)
                            f.update()
        return{'FINISHED'}

class KeyframeMiddleToLastAndFirst(bpy.types.Operator):
    """Duplicate first keyframe and move to the last """
    bl_idname = "bone.keyframemiddletolastandfirst"
    bl_label = "Unused"

    def execute(self, context):
        return{'FINISHED'}        

class MakeAnimLoop(bpy.types.Operator):
    """Make anim loop, WARNING can break custom curve handles """
    bl_idname = "bone.makeanimloop"
    bl_label = "Unused"

    def execute(self, context):
        i=0            
        secondframe = 0

        #set frame limits
        keys = action.frame_range
        lastkey=(keys[-1])
        scn.frame_end = lastkey
        
        endframe = bpy.context.scene.frame_end
        startframe  = bpy.context.scene.frame_start-1

        for fcurve in action.fcurves:
            #check to see if curve has more than 2 keyframes
            ii = 0
            for points in fcurve.keyframe_points:
                ii += 1
            if ii > 2:
                secondframe=fcurve.keyframe_points[1].co[0]
                fcurve.keyframe_points.add(1) 
                fcurve.keyframe_points[len(fcurve.keyframe_points)-1].co = (endframe+secondframe+1),(fcurve.keyframe_points[1].co[1])
                fcurve.update()

                for point in fcurve.keyframe_points:
                    
                    #set last frame to autoclamped handle mode
                    if point.co[0] == endframe:
                        point.handle_left_type="AUTO_CLAMPED"
                        point.handle_right_type="AUTO_CLAMPED"
                    fcurve.update()
                    
                     #set last frame to free handle mode
                    for point in fcurve.keyframe_points:
                        if point.co[0] == endframe:
                            point.handle_left_type="FREE"
                            point.handle_right_type="FREE"
                    fcurve.update()
                    
                     #set start frame to free handle mode
                    for point in fcurve.keyframe_points:
                        if point.co[0]== startframe:
                            point.handle_left_type="FREE"
                            point.handle_right_type="FREE"
                fcurve.update()
                
                a1=fcurve.keyframe_points[len(fcurve.keyframe_points)-2].handle_left
                a2=fcurve.keyframe_points[len(fcurve.keyframe_points)-2].co[0]
                a3=fcurve.keyframe_points[0].co[0]
              
                b1=fcurve.keyframe_points[len(fcurve.keyframe_points)-2].handle_right
                b2=fcurve.keyframe_points[len(fcurve.keyframe_points)-2].co[1]
                b3=fcurve.keyframe_points[0].co[1]      
                
                fcurve.keyframe_points[0].handle_left= a1[0]-a2+a3, a1[1]-b2+b3
                fcurve.keyframe_points[0].handle_right= b1[0]-a2+a3, b1[1]-b2+b3
                
                fcurve.update()
                fcurve.keyframe_points.remove(fcurve.keyframe_points[len(fcurve.keyframe_points)-1])
        return{'FINISHED'}

class ToggleSelectability(bpy.types.Operator):
    """Toggles all scene object selectability leaving rig always selectable """
    bl_idname = "bone.toggleselectability"
    bl_label = "Unused"

    def execute(self, context):
        do_i_hide_select = not bpy.context.active_object.hide_select
        if bpy.context.selected_objects == []:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    ob.hide_select = True
            else:
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        ob.hide_select = do_i_hide_select
        else:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        do_i_hide_select2 = not ob.hide_select
                        for ob in bpy.context.scene.objects:
                            ob.hide_select = do_i_hide_select2
                        break                
                bpy.context.object.hide_select = False
            else:
                for ob in bpy.context.selected_objects:
                    ob.hide_select = not ob.hide_select
        return{'FINISHED'}

class ToggleXray(bpy.types.Operator):
    """Toggle Xray mode """
    bl_idname = "bone.togglexray"
    bl_label = "Unused"

    def execute(self, context): 
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                obj.show_x_ray = not obj.show_x_ray
        return{'FINISHED'}


################
###### UI ######
################
    
class FrankiesAnimationTools(bpy.types.Panel):
    """Creates a custom rigging Panel in the 3D View"""
    bl_label = "Frankies Animation Tools"
    bl_idname = "POSE_PT_frankie"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rigging"
    bl_context = "posemode"  
    
    def draw(self, context):
        layout = self.layout        
    
        col = layout.column(align=True)
        col.label(text="Keyframes:")
        row = layout.row(align=True)
        
        row.operator("bone.keyframeallactions", text="Keyframe all actions")
        row = layout.row(align=True)
        row.operator("bone.removekeyframes", text="Remove all keyframes ")
        row = layout.row(align=True)
        row.operator("bone.removekeyframesapartfromone", text="Remove all but one")
        
        col = layout.column(align=True)
        col.label(text="Actions and NLA:")
        row = layout.row(align=True)
        row = col.row(align=True)  
        row.operator("bone.actionstonnlastrips", text="Actions to NLA strips")
        row = col.row(align=True)  
        row.operator("bone.unmutenlastrips", text="Unmute All")
        row.operator("bone.mutenlastrips", text="Mute All")
        row = layout.row(align=True)
        row.operator("bone.prevaction", text="Prev Action ")
        row.operator("bone.nextaction", text="Next Action")
 
        col = layout.column(align=True)
        col.label(text="Fake Users Actions:")
        row = layout.row(align=True)

        row.operator("bone.addfakeusers", text="Add F ")
        row.operator("bone.removefakeusers", text="Remove F")

        row = layout.row(align=True)
        row.operator("bone.cleananimdata", text="Clean up loose anims")

        col = layout.column(align=True)
        col.label(text="Anim Tools:")
        row = layout.row(align=True)
        
        col = layout.column(align=True)          
        row.operator("bone.makeanimloop", text="Make anim loop")
      
        row = col.row(align=True)  
        row.operator("bone.smartkeyframefix", text="Smart Keyframe Move Fix")
        row = col.row(align=True)
        row.operator("bone.keyframefirsttolast", text="First to Last")
        row.operator("bone.keyframemiddletolastandfirst", text="Middle to First and Last")
        row.operator("bone.keyframelasttofirst", text="Last to First")

        col = layout.column(align=True)       
        col.label(text="Selection and visibility:")
       
        row = layout.row(align=True)        
        row.operator("bone.togglexray", text="Toggle Xray")
        row = layout.row(align=True)
        row.operator("bone.toggleselectability", text="Toggle Selectability")
         

######################
###### REGISTER ######
###################### 
    
def register():   
    
    bpy.utils.register_class(KeyFrameAllActions)
    bpy.utils.register_class(RemoveKeyFrames)
    bpy.utils.register_class(RemoveKeyFramesApartFromOne)
    bpy.utils.register_class(ActionstOnNlaStrips)
    bpy.utils.register_class(UnmuteNlaStrips)
    bpy.utils.register_class(MuteNlaStrips)
    bpy.utils.register_class(NextAction)
    bpy.utils.register_class(PrevAction)
    bpy.utils.register_class(AddFakeUsers)
    bpy.utils.register_class(RemoveFakeUsers)
    bpy.utils.register_class(CleanAnimData)
    bpy.utils.register_class(SmartKeyframeFix)
    bpy.utils.register_class(KeyframeLastToFirst)
    bpy.utils.register_class(KeyframeFirstToLast)
    bpy.utils.register_class(KeyframeMiddleToLastAndFirst)
    bpy.utils.register_class(MakeAnimLoop)
    bpy.utils.register_class(ToggleSelectability)
    bpy.utils.register_class(ToggleXray)
    bpy.utils.register_class(FrankiesAnimationTools)


def unregister():      
    
    bpy.utils.unregister_class(KeyFrameAllActions)
    bpy.utils.unregister_class(RemoveKeyFrames)
    bpy.utils.unregister_class(RemoveKeyFramesApartFromOne)
    bpy.utils.unregister_class(ActionstOnNlaStrips)
    bpy.utils.unregister_class(UnmuteNlaStrips)
    bpy.utils.unregister_class(MuteNlaStrips)
    bpy.utils.unregister_class(NextAction)
    bpy.utils.unregister_class(PrevAction)
    bpy.utils.unregister_class(AddFakeUsers)
    bpy.utils.unregister_class(RemoveFakeUsers)
    bpy.utils.unregister_class(CleanAnimData)
    bpy.utils.unregister_class(SmartKeyframeFix)
    bpy.utils.unregister_class(KeyframeLastToFirst)
    bpy.utils.unregister_class(KeyframeFirstToLast)
    bpy.utils.unregister_class(KeyframeMiddleToLastAndFirst)
    bpy.utils.unregister_class(MakeAnimLoop)
    bpy.utils.unregister_class(ToggleSelectability)
    bpy.utils.unregister_class(ToggleXray)
    bpy.utils.unregister_class(FrankiesAnimationTools)

if __name__ == "__main__":
    register()