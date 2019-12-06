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
import random
import os
from bpy.props import *

########################
####### FUNCTIONS ######
########################

def whatsMyAction():
    i = 0

    obj = bpy.context.object                    #active object
    scn = bpy.context.scene                     #current scene

    if obj.animation_data != None:
        action = obj.animation_data.action      #current action

    for action in bpy.data.actions:
        if action.name == bpy.context.object.animation_data.action.name:
            actionindex = i
        i += 1
    return(actionindex)

#below was ripped from export_fbx_bin.py
def export_fbx_settings():
    return {
        # These options seem to produce the same result as the old Ascii exporter in Unity3D:
        "version": 'BIN7400',
        "axis_up": 'Y',
        "axis_forward": '-Z',
        #"global_matrix": Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
        # Should really be True, but it can cause problems if a model is already in a scene or prefab
        # with the old transforms.
        "bake_space_transform": False,

        "use_selection": False,

        "object_types": {'ARMATURE', 'EMPTY', 'MESH', 'OTHER'},
        "use_mesh_modifiers": True,
        "use_mesh_edges": False,
        "mesh_smooth_type": 'FACE',
        "use_tspace": False,  # XXX Why? Unity is expected to support tspace import...

        "use_armature_deform_only": True,

        "use_custom_props": True,

        "bake_anim": True,
        "bake_anim_simplify_factor": 1.0,
        "bake_anim_step": 1.0,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": True,
        "add_leaf_bones": False,  # Avoid memory/performance cost for something only useful for modelling
        "primary_bone_axis": 'Y',  # Doesn't really matter for Unity, so leave unchanged
        "secondary_bone_axis": 'X',

        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "apply_unit_scale": False,
        "apply_scale_options" : 'FBX_SCALE_ALL',
    }

def export_fbx_mesh_settings():
    return {
        # These options seem to produce the same result as the old Ascii exporter in Unity3D:
        "version": 'BIN7400',
        "axis_up": 'Y',
        "axis_forward": '-Z',
        #"global_matrix": Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
        # Should really be True, but it can cause problems if a model is already in a scene or prefab
        # with the old transforms.
        "bake_space_transform": False,

        "use_selection": False,

        "object_types": {'ARMATURE', 'EMPTY', 'MESH', 'OTHER'},
        "use_mesh_modifiers": True,
        "use_mesh_edges": False,
        "mesh_smooth_type": 'FACE',
        "use_tspace": False,  # XXX Why? Unity is expected to support tspace import...

        "use_armature_deform_only": True,

        "use_custom_props": True,

        "bake_anim": False,
        "bake_anim_simplify_factor": 1.0,
        "bake_anim_step": 1.0,
        "bake_anim_use_nla_strips": False,
        "bake_anim_use_all_actions": False,
        "add_leaf_bones": False,  # Avoid memory/performance cost for something only useful for modelling
        "primary_bone_axis": 'Y',  # Doesn't really matter for Unity, so leave unchanged
        "secondary_bone_axis": 'X',

        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "apply_unit_scale": False,
        "apply_scale_options" : 'FBX_SCALE_ALL',
    }

def export_fbx_anim_settings():
    return {
        # These options seem to produce the same result as the old Ascii exporter in Unity3D:
        "version": 'BIN7400',
        "axis_up": 'Y',
        "axis_forward": '-Z',
        #"global_matrix": Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
        # Should really be True, but it can cause problems if a model is already in a scene or prefab
        # with the old transforms.
        "bake_space_transform": False,

        "use_selection": False,

        #"object_types": {'ARMATURE', 'EMPTY', 'MESH', 'OTHER'},
        "object_types": {'ARMATURE', 'EMPTY', 'OTHER'}, #note empty object is required in the scene or else unity breaks hierarchy by nurfing rig object and going straight to root
        "use_mesh_modifiers": True,
        "use_mesh_edges": False,
        "mesh_smooth_type": 'FACE',
        "use_tspace": False,  # XXX Why? Unity is expected to support tspace import...

        "use_armature_deform_only": True,

        "use_custom_props": True,

        "bake_anim": True,
        "bake_anim_simplify_factor": 1.0,
        "bake_anim_step": 1.0,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": False,
        "add_leaf_bones": False,  # Avoid memory/performance cost for something only useful for modelling
        "primary_bone_axis": 'Y',  # Doesn't really matter for Unity, so leave unchanged
        "secondary_bone_axis": 'X',

        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "apply_unit_scale": False,
        "apply_scale_options" : 'FBX_SCALE_ALL',
    }

def export_fbx_anim_multiple_settings():
    return {
        # These options seem to produce the same result as the old Ascii exporter in Unity3D:
        "version": 'BIN7400',
        "axis_up": 'Y',
        "axis_forward": '-Z',
        #"global_matrix": Matrix.Rotation(-math.pi / 2.0, 4, 'X'),
        # Should really be True, but it can cause problems if a model is already in a scene or prefab
        # with the old transforms.
        "bake_space_transform": False,

        "use_selection": False,

        "object_types": {'ARMATURE', 'EMPTY', 'MESH', 'OTHER'},
        #"object_types": {'ARMATURE', 'EMPTY', 'OTHER'}, #note empty object is required in the scene or else unity breaks hierarchy by nurfing rig object and going straight to root
        "use_mesh_modifiers": True,
        "use_mesh_edges": False,
        "mesh_smooth_type": 'FACE',
        "use_tspace": False,  # XXX Why? Unity is expected to support tspace import...

        "use_armature_deform_only": True,

        "use_custom_props": True,

        "bake_anim": True,
        "bake_anim_simplify_factor": 1.0,
        "bake_anim_step": 1.0,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": False,
        "add_leaf_bones": False,  # Avoid memory/performance cost for something only useful for modelling
        "primary_bone_axis": 'Y',  # Doesn't really matter for Unity, so leave unchanged
        "secondary_bone_axis": 'X',

        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "apply_unit_scale": False,
        "apply_scale_options" : 'FBX_SCALE_ALL',
    }    

def export_fbx():
    
    sceneexportpath = bpy.context.scene.FbxExportPath
    
    if sceneexportpath == "":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\"

    if sceneexportpath[:2] == "..":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\" + sceneexportpath

    exportpath = sceneexportpath + bpy.context.scene.name +".fbx"
    print (exportpath)
    bpy.ops.export_scene.fbx(filepath=exportpath, **export_fbx_settings())
    return()

def export_fbx_mesh():

    framenumber =""
    sceneexportpath = bpy.context.scene.FbxExportPath

    if sceneexportpath == "":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\"

    if sceneexportpath[:2] == "..":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\" + sceneexportpath

    if bpy.context.scene.AnimMiddleFix == "FRAME":
        framenumber = "{:02d}".format(bpy.context.scene.frame_current)

    exportpath = sceneexportpath + bpy.context.scene.name + framenumber +".fbx"
    bpy.ops.export_scene.fbx(filepath=exportpath, **export_fbx_mesh_settings())
    return()

def export_fbx_anim():
    obj = bpy.context.object                    #active object
    scn = bpy.context.scene                     #current scene

    currentaction = bpy.context.object.animation_data.action
    currentscene = bpy.context.scene

    if sceneexportpath == "":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\"

    if sceneexportpath[:2] == "..":
        filepath = bpy.data.filepath
        sceneexportpath = os.path.dirname(filepath) + "\\" + sceneexportpath

    exportpath = sceneexportpath + bpy.context.scene.name +".fbx"

    #sets correct mute and unmuting
    for nlatrack in bpy.context.object.animation_data.nla_tracks:
        bpy.context.object.animation_data.nla_tracks.remove(nlatrack)

    for action in bpy.data.actions:
        print(action)
        bpy.context.object.animation_data.nla_tracks.new()
        bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].name = action.name
        bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].strips.new(action.name,0,action)
        bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].mute = not action.Export

    #set strips set to mute
    for a in obj.animation_data.nla_tracks:
        a.strips[0].mute=True
        
    bpy.context.scene.update()  #update
    
    #go though strips set it to true, export fbx with strip name then set back to false
    for a in obj.animation_data.nla_tracks:
        #dont export strips with $ at the end
        if a.name[-1:] != "$":
            # check to see if track is muted, if it is dont bother exporting it
            if a.mute != True:
                print ("**  exporting action", a.name)
                #check speed bone and change scene fps for export
                for act in bpy.data.actions:
                    if a.name == act.name:
                        for fcurve in bpy.data.actions[act.name].fcurves:
                            b = (str(fcurve.data_path))
                            if "speed" in b:
                                if "location" in b:
                                    if fcurve.array_index == 1:
                                        framerange = fcurve.keyframe_points[len(fcurve.keyframe_points)-1].co[0] - fcurve.keyframe_points[0].co[0]#-1
                                        distance = fcurve.keyframe_points[len(fcurve.keyframe_points)-1].co[1] - fcurve.keyframe_points[0].co[1]
                                        if distance > 0:
                                            print ("fps =",(2/distance) * framerange)
                                            currentscene.render.fps = int((2/distance)*framerange)
                                        else:
                                            print ("no speed data found, fps 30")
                                            currentscene.render.fps = 30
                #sets action to be the same as clip name in the stash
                bpy.context.object.animation_data.action = bpy.data.actions[a.strips[0].name]
                #makes a strip unmuted
                a.strips[0].mute=False
                bpy.context.scene.update() #update
                filenametoexport = str(a.strips[0].name)
                filenametoexport = filenametoexport.replace(bpy.context.scene.name, bpy.context.scene.name + bpy.context.scene.AnimMiddleFix)
                exportpathanim = bpy.context.scene.FbxExportPath + "\\" + filenametoexport + ".fbx"
                bpy.ops.export_scene.fbx(filepath=exportpathanim, **export_fbx_anim_settings())
                    #mute strip again so it dosent get exported with next strip
                a.strips[0].mute=True
                bpy.context.scene.update()  #update  

    currentscene.render.fps = 30
    bpy.context.object.animation_data.action = currentaction
    return()

def export_fbx_anim_multiple():
    obj = bpy.context.object                    #active object
    scn = bpy.context.scene                     #current scene

    currentaction = bpy.context.object.animation_data.action
    currentscene = bpy.context.scene

    exportpath = bpy.context.scene.FbxExportPath + bpy.context.scene.name +  bpy.context.scene.AnimMiddleFix + ".fbx"

    #sets correct mute and unmuting

    for nlatrack in bpy.context.object.animation_data.nla_tracks:
            bpy.context.object.animation_data.nla_tracks.remove(nlatrack)
            
    for action in bpy.data.actions:
        if action.Export == True:
            print(action)
            bpy.context.object.animation_data.nla_tracks.new()
            bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].name = action.name
            bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].strips.new(action.name,0,action)
            bpy.context.object.animation_data.nla_tracks[(len(bpy.context.object.animation_data.nla_tracks)-1)].mute = not action.Export
            
            bpy.context.scene.update() #update            
            
    bpy.ops.export_scene.fbx(filepath=exportpath, **export_fbx_anim_multiple_settings())
        #mute strip again so it dosent get exported with next strip
    bpy.context.scene.update()  #update
               
    bpy.context.object.animation_data.action = currentaction
    return()       
    
def export_fbx_anim_old():
    obj = bpy.context.object                    #active object
    scn = bpy.context.scene                     #current scene

    currentaction = bpy.context.object.animation_data.action
    currentscene = bpy.context.scene

    exportpath = bpy.context.scene.FbxExportPath + bpy.context.scene.name +".fbx"
    #go though strips set it to true, export fbx with strip name then set back to false
    for a in obj.animation_data.nla_tracks:
        #dont export strips with $ at the end
        if a.name[-1:] != "$":
            #always export active action
            if currentaction.name == a.name:
                a.mute = False
                print(a.name)
            # check to see if track is muted, if it is dont bother exporting it
            if a.mute == False:
                print ("**  exporting action", a.name)
                #check speed bone and change scene fps for export
                for act in bpy.data.actions:
                    if a.name == act.name:
                        for fcurve in bpy.data.actions[act.name].fcurves:
                            b = (str(fcurve.data_path))
                            if "speed" in b:
                                if "location" in b:
                                    if fcurve.array_index == 1:
                                        framerange = fcurve.keyframe_points[len(fcurve.keyframe_points)-1].co[0] - fcurve.keyframe_points[0].co[0]#-1
                                        distance = fcurve.keyframe_points[len(fcurve.keyframe_points)-1].co[1] - fcurve.keyframe_points[0].co[1]
                                        if distance > 0:
                                            #print ("fps =",(2/distance) * framerange)
                                            currentscene.render.fps = int((2/distance)*framerange)
                                        else:
                                            currentscene.render.fps = 30
                #sets action to be the same as clip name in the stash
                bpy.context.object.animation_data.action = bpy.data.actions[a.strips[0].name]
                #makes a strip unmuted
                a.strips[0].mute=False
                bpy.context.scene.update() #update
                filenametoexport = str(a.strips[0].name)
                filenametoexport = filenametoexport.replace(bpy.context.scene.name, bpy.context.scene.name + bpy.context.scene.AnimMiddleFix)
                exportpathanim = bpy.context.scene.FbxExportPath + "\\" + filenametoexport + ".fbx"
                bpy.ops.export_scene.fbx(filepath=exportpathanim, **export_fbx_anim_settings())
                    #mute strip again so it dosent get exported with next strip
                a.strips[0].mute=True
                bpy.context.scene.update()  #update
    #leave all strips set to mute
    for a in obj.animation_data.nla_tracks:
        a.strips[0].mute=True

    currentscene.render.fps = 30
    bpy.context.object.animation_data.action = currentaction
    return()

def copyModifier(source, target):
    active_object = source
    obj = target

    for mSrc in active_object.modifiers:
        mDst = obj.modifiers.get(mSrc.name, None)
        if not mDst:
            mDst = obj.modifiers.new(mSrc.name, mSrc.type)

        # collect names of writable properties
        properties = [p.identifier for p in mSrc.bl_rna.properties
                      if not p.is_readonly]

        # copy those properties
        for prop in properties:
            setattr(mDst, prop, getattr(mSrc, prop))
            
def vertexColor():
    # start in object mode
    obj = bpy.context.selected_objects

    for o in obj:
        mesh = o.data
        
        if not mesh.vertex_colors:
            mesh.vertex_colors.new()

        """
        let us assume for sake of brevity that there is now 
        a vertex color map called  'Col'    
        """

        color_layer = mesh.vertex_colors["Col"]

        # or you could avoid using the color_layer name
        # color_layer = mesh.vertex_colors.active  
        i = 0

        value = o.name[-3:]
        try:
            value = float(value)
        except:
            value = 0
            
        print (o.name + " getting value " + str(value))
        value = value / 255

        rgb = [value,value,value]

        for poly in mesh.polygons:
            for idx in poly.loop_indices:
                color_layer.data[i].color = rgb
                i += 1


        # set to vertex paint mode to see the result
        # bpy.ops.object.mode_set(mode='VERTEX_PAINT')

def mergeGroups(dovc):
    print ("-----------------------------")
    scn = bpy.context.scene
    selobj = bpy.context.selected_objects
    doExecute = True
    groups = []

    #check seleted objects have groups
    for group in bpy.data.groups:
        for o in selobj:
            if group.name == o.name:
                #make a list of all objects in group
                print ("starting " + group.name)
                objInGroup = []
                for obj in group.objects:
                    if obj.type == "MESH":
                        objInGroup.append(obj)

                #find object corresponding to group (object to replace has to be named the same as group)
                for obj in bpy.data.objects:
                    if obj.name == group.name:
                        print("found object for "+ obj.name)
                        oldObj = obj
                        oldObjmatrix = obj.matrix_world
                        objName = obj.name
                    
                #go though list of objects and..
                objInGroupNew = []
                for obj in objInGroup:
                    print ("obj name = " + obj.name) 
                    if obj.name != objName:
                        objData = obj.data.copy()         #get data from object

                        ob = bpy.data.objects.new("MergeMe"+ obj.name[-4:], objData)   #add that data to a new object
                        ob.matrix_world = obj.matrix_world              #in the same place as the old one
                                             
                        scn.objects.link(ob)        #add to scene
                        objInGroupNew.append(ob)    #add to list of NEW objects
                        copyModifier(obj,ob)
                        
                        scn.update()        

                #rename old object ready for delete
                oldObj.name = "DELETEME"

                # select all new objects
                for obj in bpy.data.objects:
                    for objG in objInGroupNew:
                        if obj.name in objG.name:
                            obj.select = True 
                            bpy.context.scene.objects.active = obj
                            break
                        obj.select = False
                        
                #apply modifiers(have been copied)
                bpy.ops.object.convert(target='MESH')

                #apply scale and transform info
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                                            
                #make a new object to merge all new objects into, add to scene and set transform based on old one
                me = bpy.data.meshes.new(group.name)
                ob = bpy.data.objects.new(group.name, me)
                scn.objects.link(ob)
                ob.matrix_world = oldObjmatrix
                
                if dovc == True:
                    vertexColor()

                #select this new object
                ob.select = True
                bpy.context.scene.objects.active = ob  #has to be active so join works

                #merge all new objects into one
                bpy.ops.object.join()

                #copy layer info and modifiers from old models to new one
                ob.layers = oldObj.layers
                oldObj.select = True
                bpy.context.scene.objects.active = oldObj
                bpy.ops.object.make_links_data(type="MODIFIERS")

                #remove old object
                scn.objects.unlink(oldObj)
                oldObj.user_clear()
                scn.update()

                print("finished " + group.name)

def namebyheight(gbhname):
    selobjects = bpy.context.selected_objects    
    if gbhname == None:
        activeobject = bpy.context.active_object
        name = activeobject.name
    else:
        name = gbhname + gbhname
    ypos = -10
    number = 1
    objectsYarray = []

    if name[-3:].isdigit():
        name = name[:-4]
    
    for object in selobjects:
        object.name = "temp"
    
    for object in selobjects:
        #reset the array
        objectsYarray = []
        #find objects higher than active object
        for object in selobjects:
            if object.matrix_world[2][3] > ypos:
                objectsYarray.append(object)
            
            #in objects that are higher, find lowest
            higherYobjectsMinPos = 100000        
            for higherYobjects in objectsYarray:
                if higherYobjects.matrix_world[2][3] < higherYobjectsMinPos:
                    higherYobjectsMinPos = higherYobjects.matrix_world[2][3]
            
        #loop though objects again, if object y pos = it must be the next highest so rename it
        for object in selobjects:
            if object.matrix_world[2][3] == higherYobjectsMinPos:
                # print("lowest object is", object.name ," at ", higherYobjectsMinPos)
                # this bit is because the naming convention needs to be 3 digits but that data isnt stored anywhere
                if len(str(number)) == 1:
                    stringnumber = "00"+str(number)
                if len(str(number)) == 2:
                    stringnumber = "0"+str(number)
                if len(str(number)) == 3:
                    stringnumber = str(number)

                object.name = name + "." + stringnumber
                number += 1
                ypos = higherYobjectsMinPos

def namebyheightgroup():
    selobj = bpy.context.selected_objects
    #activeobject = bpy.context.active_object
        
    #for objects in group
    for group in bpy.data.groups:
        for o in selobj:
            if group.name == o.name:
                bpy.ops.object.select_all(action="DESELECT")
                for obj in group.objects:
                    obj.select = True
                    bpy.context.scene.objects.active = obj
                namebyheight(group.name)
                
    #bpy.ops.object.select_all(action="DESELECT")
    #remeber old sel and active objects
    #bpy.context.selected_objects = selobj
    #bpy.context.active_object = activeobject

#######################
###### OPERATORS ######
#######################

class AutoMergeGroups(bpy.types.Operator):
    """Replaces mesh of object name X with all objects in group name X"""
    bl_idname = "bone.automergegroups"
    bl_label = "Unused"

    def execute(self, context):
        mergeGroups(False)
        return{'FINISHED'}

class AutoMergeGroupsVC(bpy.types.Operator):
    """Replaces mesh of object name X with all objects in group name X, do vertex colouring based on object name so you can use it on objects with no mesh data, like remesh or skin modifiers"""
    bl_idname = "bone.automergegroupsvc"
    bl_label = "Unused"

    def execute(self, context):
        mergeGroups(True)
        return{'FINISHED'}

class AutoMergeGroupsNameVC(bpy.types.Operator):
    """Replaces mesh of object name X with all objects in group name X, do vertex colouring based on object name so you can use it on objects with no mesh data, like remesh or skin modifiers"""
    bl_idname = "bone.automergegroupsnamevc"
    bl_label = "Unused"

    def execute(self, context):
        print("7777777777777777777777777")
        ao = bpy.context.scene.objects.active.name
        print (ao)
        selobj = bpy.context.selected_objects

        namebyheightgroup()

        bpy.ops.object.select_all(action="DESELECT")
        for obj in selobj:
            obj.select = True
                
        mergeGroups(True)
        """
        for obj in bpy.data.objects:
            if obj.name == ao:
                bpy.context.scene.objects.active = obj
        """
        return{'FINISHED'}

class NameByHeight(bpy.types.Operator):
    """Name objects based on height"""
    bl_idname = "bone.namebyheight"
    bl_label = "Unused"

    def execute(self, context):
        namebyheight(None)
        return{'FINISHED'}

class VertexValueByName(bpy.types.Operator):
    """ Take last 3 didgets of the object name and set them to be the vertex colour for the object, eg verts in the object name.023 gets the vertex value 023, 023, 023 """
    bl_idname = "bone.vertexvaluebyname"
    bl_label = "Unused"
    
    def execute(self, context):
        vertexColor()
        return{'FINISHED'}


class KeyFrameAllActions(bpy.types.Operator):
    """Propogate first keyframe from this action to all other actions if that action is missing a keyframe, handy for when you add a new bone and now need a keyframe for it on all other actions """
    bl_idname = "bone.keyframeallactions"
    bl_label = "Unused"
    
    def execute(self, context):
    
        obj = bpy.context.object             #active object
        action = obj.animation_data.action   #current action  
        print ("--start--")

        for selbone in bpy.context.selected_pose_bones:
            print ("for bone,", selbone.name)
            sb = str(selbone)
            sbn = str("\""+selbone.name+"\"")
            i=0   
            fcurvepath=[]
            fcurvepathindex=[]  
            kfpvalue=[]
            fcgroup=[]

            #create a list of f curve indexs the selected bone uses, bones must allready have keys for this to work
            for f in bpy.data.actions[action.name].fcurves:
                fstr = (str(f.data_path))
                if sbn in fstr:                                 #this creates an array with all the info to copy to new actions           
                    fcurvepath.append(f.data_path)              #save fcurve name
                    fcurvepathindex.append(f.array_index)       #save fcurve index
                    kfpvalue.append(f.keyframe_points[0].co)    #save fcurve data values                       
                    if f.group == None:                         #if no group make a new one
                        fcgroup.append("controllers")           #save fcurve group, madeup name
                    else:
                        fcgroup.append(f.group.name)            #save fcurve group, real name

            #go though all actions check to see if fcurve data exists if not make new curves from above data
            for a in bpy.data.actions:
                booltest = False
                i=0       
                for f in bpy.data.actions[a.name].fcurves: 
                    b = (str(f.data_path))                    
                    if sbn in b and booltest == False:
                        print (a.name, " allready has fcruve data for", selbone.name,"skipping")
                        booltest = True                 #this only checks for one instance of the fcurve, could return false positives if only one chanel had a keyframe
                
                if booltest == False:
                    print (a.name, " has no data for", selbone.name,"adding")            
                    for fcp in fcurvepath:
                        kfp = a.fcurves.new(fcp, fcurvepathindex[i],fcgroup[i])     
                        kfp.keyframe_points.add(1)
                        kfp.keyframe_points[0].co = kfpvalue[i]                                             
                        i += 1    
      
        return{'FINISHED'}
        
        
class KeyFrameAllActionsConstraints(bpy.types.Operator):
    """Propogate first keyframe from this action to all other actions if that action is missing a keyframe, handy for when you add a new bone and now need a keyframe for it on all other actions """
    bl_idname = "bone.keyframeallactionsconstraints"
    bl_label = "Unused"
    
    def execute(self, context):
        action = bpy.context.object.animation_data.action   #current action  
        actions = bpy.data.actions

        print ("--------")
        for selbone in bpy.context.selected_pose_bones:
            print ("for bone,", selbone.name)   
            sbn = str("\""+selbone.name+"\"")   

            for f in bpy.data.actions[action.name].fcurves:
                fstr = (str(f.data_path))
                if sbn in fstr:
                    findex = f.data_path
                    if "constraint" in findex:
                        print(findex)
                        for a in actions:
                            print ("--------")
                            booltest = False
                            print ("Action = "+a.name)
                            for f in bpy.data.actions[a.name].fcurves: 
                                b = (str(f.data_path))
                                if findex in  b:
                                    print (b, " found, moving on to next animation")
                                    booltest = True 
                            if booltest == False:
                                print ("Didnt find it, adding")
                                kfp = a.fcurves.new(findex)
                                kfp.keyframe_points.add(1)
                                kfp.keyframe_points[0].co = 0.0, 0.0
                                booltest = True                      
        return{'FINISHED'}        

class RemoveKeyFrames(bpy.types.Operator):
    """ Remove se bone keyframes from all actions """
    bl_idname = "bone.removekeyframes"
    bl_label = "Unused"

    def execute(self, context):
        selectedBoneList = []
              
        if bpy.context.scene.SelBoneOnly == False:
            for a in bpy.data.armatures[0].bones:
                selectedBoneList.append([a,a.select])
                a.select = True
                
        for selbone in bpy.context.selected_pose_bones:
            bone_path = '"' + selbone.name + '"'
            #for fc in action.fcurves:
            for a in bpy.data.actions:
                if a.Export == True:
                    for fc in a.fcurves:
                        if bone_path not in fc.data_path:
                            continue
                        while len(fc.keyframe_points):
                            fc.keyframe_points.remove(fc.keyframe_points[0])
                        
        if bpy.context.scene.SelBoneOnly == False:
            for i in selectedBoneList:
                i[0].select = i[1]         
        
        #now go though and remove emtpy groups
        action = bpy.context.object.animation_data.action   #current action  
        actions = bpy.data.actions
       
        for selbone in bpy.context.selected_pose_bones:
            print ("for bone,", selbone.name)   
            sbn = str("\""+selbone.name+"\"")   

            for f in bpy.data.actions[action.name].fcurves:
                fstr = (str(f.data_path))
                if sbn in fstr:
                    findex = f.data_path
                    for a in actions:
                        booltest = False
                        for f in a.fcurves:
                            if len(f.keyframe_points) == 0:
                                a.fcurves.remove(f)
        return{'FINISHED'}

class RemoveKeyFramesApartFromOne(bpy.types.Operator):
    """Remove all but a single non specific keyframe on actions flted above"""
    bl_idname = "bone.removekeyframesapartfromone"
    bl_label = "Unused"

    def execute(self, context):
        selectedBoneList = []
              
        if bpy.context.scene.SelBoneOnly == False:
            for a in bpy.data.armatures[0].bones:
                selectedBoneList.append([a,a.select])
                a.select = True
                
        for action in bpy.data.actions:            
            if action.Export == True:
                for fcurve in action.fcurves:
                    i = 0
                    for keyframepoint in fcurve.keyframe_points:                            
                        if keyframepoint.co[0] != 0:                     
                            fcurve.keyframe_points.remove(fcurve.keyframe_points[i])
                            i -= 1
                        i += 1                        
                            
        if bpy.context.scene.SelBoneOnly == False:
            for i in selectedBoneList:
                i[0].select = i[1]     
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
        for nlatrack in bpy.context.object.animation_data.nla_tracks:
            bpy.context.object.animation_data.nla_tracks.remove(nlatrack)
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
        action = bpy.context.object.animation_data.action   #current action  
        
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
        action = bpy.context.object.animation_data.action   #current action  
        
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

class ToggleActionExport(bpy.types.Operator):
    """Toggle Action Export """
    bl_idname = "bone.toggleactionexport"
    bl_label = "Unused"

    def execute(self, context):
        
        trueorfalse = bpy.data.actions[0].Export 
        for action in bpy.data.actions:
            action.Export = not trueorfalse
        return{'FINISHED'}        

class FbxExportMesh(bpy.types.Operator):
    """Export mesh data only"""
    bl_idname = "bone.fbxexportmesh"
    bl_label = "Unused"

    def execute(self, context):
        export_fbx_mesh()
        return{'FINISHED'}

export_fbx_anim_multiple        

class FbxExportAnimMultiple(bpy.types.Operator):

    """Export only anims that are unmuted in the NLA editor to one fbx"""
    bl_idname = "bone.fbxexportanimmultiple"
    bl_label = "Unused"

    def execute(self, context):
        export_fbx_anim_multiple()
        return{'FINISHED'}
        
class FbxExportAnim(bpy.types.Operator):

    """Export only anims that are unmuted in the NLA editor"""
    bl_idname = "bone.fbxexportanim"
    bl_label = "Unused"

    def execute(self, context):
        export_fbx_anim()
        return{'FINISHED'}

class FbxExport(bpy.types.Operator):
    """Export All"""
    bl_idname = "bone.fbxexport"
    bl_label = "Unused"

    def execute(self, context):
        export_fbx()
        return{'FINISHED'}

class FActionList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if bpy.context.active_object != None:
            row = layout.row(False)
            row.prop(item,"name", text = "", emboss= False)
            row.prop(item,"Export", text = "");


################
###### UI ######
################

class FrankiesExportPopupMenu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        """
        layout = self.layout
        obj = context.object

        col = layout.column(align=True)
        row = layout.row(align=True)

        row.label(text="Fbx Export to :")
        row.label(text= bpy.context.scene.FbxExportPath + bpy.context.scene.name +".fbx")
        row = layout.row(align=True)
        row.prop(context.scene, "FbxExportPath")
        row = layout.row(align=True)
        row.prop(context.scene, "name", text="Filename")
        row = layout.row(align=True)
        row.prop(context.scene, "AnimMiddleFix")
        row = layout.row(align=True)

        row.operator("bone.fbxexportmesh", text="Export Mesh")
        row.operator("bone.fbxexportanim", text="Export Animations")
        row.operator("bone.fbxexport", text="Export All")

        layout.template_list("FActionList", "", bpy.data, "actions", obj, "action_list_index", rows=2)
        row = layout.row(align=True)
        row.operator("bone.toggleactionexport", text="Toggle")
        """
        
        layout = self.layout
        layout.label(text="Fbx Export to :")
        layout.label(text= bpy.context.scene.FbxExportPath + bpy.context.scene.name +".fbx")
#        layout.prop(context.scene, "name", text="Filename")
        layout.prop(context.scene, "FbxExportPath")

        layout.prop(context.scene, "AnimMiddleFix")


        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True

        layout.operator("object.shade_smooth")

        layout.label(text="Hello world!", icon='WORLD_DATA')

        # use an operator enum property to populate a sub-menu
        layout.operator_menu_enum("object.select_by_type",
                                  property="type",
                                  text="Select All by Type...",
                                  )

        # call another menu
        layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"
        


class FrankiesAnimationTools(bpy.types.Panel):
    """Creates a custom rigging Panel in the 3D View"""
    bl_label = "Frankies Animation Tools"
    bl_idname = "POSE_PT_frankie"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rigging"
    bl_context = "posemode"

    bpy.types.Scene.FbxExportPath = bpy.props.StringProperty(name = "Path")
    bpy.types.Scene.AnimMiddleFix = bpy.props.StringProperty(name = "Anim String")
    bpy.types.Scene.LastAnimSelected = bpy.props.StringProperty(name = "Last Anim Selected")
    bpy.types.Action.Export = bpy.props.BoolProperty(name= "Export")
    
    bpy.types.Scene.SelBoneOnly = bpy.props.BoolProperty(name= "Selected Bone Only")

    def draw(self, context):
        layout = self.layout
        obj = context.object

        col = layout.column(align=True)
        row = layout.row(align=True)

        row.label(text="Fbx Export to :")
        row.label(text= bpy.context.scene.FbxExportPath + bpy.context.scene.name +".fbx")
        row = layout.row(align=True)
        row.prop(context.scene, "FbxExportPath")
        row = layout.row(align=True)
        row.prop(context.scene, "name", text="Filename")
        row = layout.row(align=True)
        row.prop(context.scene, "AnimMiddleFix")
        row = layout.row(align=True)

        row.operator("bone.fbxexportmesh", text="Export Mesh")
        row.operator("bone.fbxexportanim", text="Export Animations")
        row = layout.row(align=True)       
        row.operator("bone.fbxexportanimmultiple", text="Export Animations Single Fbx")
        row.operator("bone.fbxexport", text="Export All")

        layout.template_list("FActionList", "", bpy.data, "actions", obj, "action_list_index", rows=2)
        if bpy.types.Scene.LastAnimSelected != bpy.data.actions[bpy.context.object.action_list_index]:
            bpy.context.object.animation_data.action = bpy.data.actions[bpy.context.object.action_list_index]
            currentaction = bpy.context.object.animation_data.action
            keys = currentaction.frame_range
            lastkey=(keys[-1])
            bpy.context.scene.frame_end = lastkey            
        bpy.types.Scene.LastAnimSelected = bpy.data.actions[bpy.context.object.action_list_index] #lets you selected with the action dropdown from action editor
        row = layout.row(align=True)
        row.operator("bone.toggleactionexport", text="Toggle")

        col = layout.column(align=True)
        row = layout.row(align=True)
        col.label(text="Keyframes:")
        col.operator("bone.keyframeallactions", text="Add missing first keyframe to other actions")
        col.operator("bone.keyframeallactionsconstraints", text="Add missing constraints first keyframe to other actions")
        col.operator("bone.removekeyframes", text="Remove keyframes on filtered actions")
        col.operator("bone.removekeyframesapartfromone", text="Remove all but first keyframe on filtered actions")
        
        row.prop(context.scene, "SelBoneOnly")
        
        col = layout.column(align=True)
        col.label(text="Actions:")

        row = layout.row(align=True)
        row.operator("bone.prevaction", text="Prev Action ")
        row.operator("bone.nextaction", text="Next Action")

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
        col.label(text="Actions and NLA:")
        row = layout.row(align=True)
        row = col.row(align=True)
        row.operator("bone.actionstonnlastrips", text="Actions to NLA strips")
        row = col.row(align=True)
        row.operator("bone.unmutenlastrips", text="Unmute All")
        row.operator("bone.mutenlastrips", text="Mute All")

        col = layout.column(align=True)
        col.label(text="Selection and visibility:")

        row = layout.row(align=True)
        row.operator("bone.togglexray", text="Toggle Xray")
        row = layout.row(align=True)
        row.operator("bone.toggleselectability", text="Toggle Selectability")
        row = layout.row(align=True)
        row.prop(obj, "hide", text="hide obje")
        row.prop(obj, "hide_select", text="hide select")
        row.prop(context.object, "hide_render")

class FrankiesAnimationToolsObject(bpy.types.Panel):
    """Creates a custom Object Panel in the 3D View"""
    bl_label = "Frankies FBX Export Tools"
    bl_idname = "ObjectPT_frankie"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Export FBX"
    bl_context = "objectmode"

    bpy.types.Scene.FbxExportPath = bpy.props.StringProperty(name = "Path")
    bpy.types.Scene.AnimMiddleFix = bpy.props.StringProperty(name = "Anim String")
    bpy.types.Action.Export = bpy.props.BoolProperty(name= "Export")
    bpy.types.Scene.SelBoneOnly = bpy.props.BoolProperty(name= "Selected Bone Only")

    def draw(self, context):
        layout = self.layout
        obj = context.object

        col = layout.column(align=True)
        row = layout.row(align=True)

        row.label(text="Fbx Export to :")
        row.label(text= bpy.context.scene.FbxExportPath + bpy.context.scene.name +".fbx")
        row = layout.row(align=True)
        row.prop(context.scene, "FbxExportPath")
        row = layout.row(align=True)
        row.prop(context.scene, "name", text="Filename")
        row = layout.row(align=True)
        row.prop(context.scene, "AnimMiddleFix")
        row = layout.row(align=True)

        row.operator("bone.fbxexportmesh", text="Export Mesh")
        row.operator("bone.fbxexportanim", text="Export Animations")
        row.operator("bone.fbxexport", text="Export All")

        if bpy.context.scene.objects.active != None:
            layout.template_list("FActionList", "", bpy.data, "actions", obj, "action_list_index", rows=2)
        row = layout.row(align=True)
        row.operator("bone.toggleactionexport", text="Toggle")
        row = layout.row(align=True)
        
        col = layout.column(align=True)
        col.label(text="Vertex Colours:")

        row = layout.row(align=True)
        row.operator("bone.namebyheight", text="Name Objects By Height")
        row = layout.row(align=True)
        row.operator("bone.vertexvaluebyname", text="Vertex Colour Objects By Height")
        row = layout.row(align=True)
        row.operator("bone.automergegroups", text="AutoMerge Groups to Objects")
        row = layout.row(align=True)
        row.operator("bone.automergegroupsvc", text="Vertex Color & AutoMerge ")
        row = layout.row(align=True)
        row.operator("bone.automergegroupsnamevc", text="Name, VC & Merge ")
        row = layout.row(align=True)

#def draw_item(self, context):
#    layout = self.layout
#    layout.menu(FrankiesExportPopupMenu.bl_idname)

######################
###### REGISTER ######
######################

def register():

    bpy.types.Object.action_list_index = bpy.props.IntProperty()
    bpy.utils.register_class(FrankiesExportPopupMenu)
    bpy.utils.register_class(KeyFrameAllActions)
    bpy.utils.register_class(KeyFrameAllActionsConstraints)
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
    bpy.utils.register_class(FbxExportMesh)
    bpy.utils.register_class(FbxExportAnim)
    bpy.utils.register_class(FbxExportAnimMultiple)
    bpy.utils.register_class(FbxExport)
    bpy.utils.register_class(FActionList)
    bpy.utils.register_class(ToggleActionExport)
    bpy.utils.register_class(FrankiesAnimationToolsObject)
    bpy.utils.register_class(FrankiesAnimationTools)
    bpy.utils.register_class(NameByHeight)
    bpy.utils.register_class(VertexValueByName)
    bpy.utils.register_class(AutoMergeGroups)
    bpy.utils.register_class(AutoMergeGroupsVC)
    bpy.utils.register_class(AutoMergeGroupsNameVC)

def unregister():

    bpy.utils.unregister_class(FrankiesExportPopupMenu)
    bpy.utils.unregister_class(KeyFrameAllActions)
    bpy.utils.unregister_class(KeyFrameAllActionsConstraints)
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
    bpy.utils.unregister_class(FbxExportMesh)
    bpy.utils.unregister_class(FbxExportAnim)
    bpy.utils.unregister_class(FbxExportAnimMultiple)
    bpy.utils.unregister_class(FbxExport)
    bpy.utils.unregister_class(FActionList)
    bpy.utils.unregister_class(ToggleActionExport)    
    bpy.utils.unregister_class(FrankiesAnimationToolsObject)
    bpy.utils.unregister_class(FrankiesAnimationTools)
    bpy.utils.unregister_class(NameByHeight)
    bpy.utils.unregister_class(VertexValueByName)
    bpy.utils.unregister_class(AutoMergeGroups)
    bpy.utils.unregister_class(AutoMergeGroupsVC)
    bpy.utils.unregister_class(AutoMergeGroupsNameVC)
    del bpy.types.Object.action_list_index

if __name__ == "__main__":
    register()  
#    bpy.ops.wm.call_menu(name=FrankiesExportPopupMenu.bl_idname)
