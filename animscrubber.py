bl_info = {
    "name": "F Anim Scrubber",
    "author": "Frankie",
    "version": (1, 7),
    "blender": (2, 76, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Drag keyframes",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
    }

import bpy

class AnimScrubber(bpy.types.Operator):
    bl_idname = "anim.scrubber"
    bl_label = "Scrub or Drag Keyframe"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        print("-------anim.scrubber start------")
    def __del__(self):
        print("anim.scrubber end")

#    def execute(self, context):
#       print (self.value)
#       bpy.context.scene.frame_current = self.value 
  
    def modal(self, context, event):
        self.valued = event.mouse_x / 10
        if event.type == 'MOUSEMOVE':  #move frames
            if bpy.context.scene.frame_current > bpy.context.scene.frame_end:
                bpy.context.scene.frame_set(bpy.context.scene.frame_start)
                self.looped += 1
            elif bpy.context.scene.frame_current < bpy.context.scene.frame_start:
                bpy.context.scene.frame_set(bpy.context.scene.frame_end)
                self.looped -= 1
            else:
                bpy.context.scene.frame_set(self.valued - self.dampedvalue + self.sframe - (bpy.context.scene.frame_end*self.looped))
#            self.execute(context)
        elif event.type == 'LEFTMOUSE' and event.value == "RELEASE":  # Confirm
            return {'FINISHED'}
        elif event.type == 'Z':  #Add motion paths
                #sets last keyframe based on action length       
            bpy.ops.pose.paths_clear()
            scn = bpy.context.scene
            if bpy.data.actions:
                if bpy.context.scene.use_preview_range == True: 
                    bpy.context.scene.use_preview_range = False #fix this to do something else in this situation
                currentaction = bpy.context.object.animation_data.action
                keys = currentaction.frame_range
                lastkey=(keys[-1])
                scn.frame_end = lastkey
                print ("actions")
            else:
                print ("no actions")            
                #turns on motion curves but dosent update if selection hasnt changed
            
            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=lastkey+1, bake_location='HEADS')
            """
            obj = (bpy.context.scene)
            if 'SceneBonelist' in obj:
                print ("SceneBonelist is allready there")
                self.bonelist = []
                if bpy.data.actions:
                    for bone in bpy.context.selected_pose_bones:
                        self.bonelist.append(bone.name)
                    if self.bonelist != bpy.context.scene["SceneBonelist"]:
                        bpy.ops.pose.select_all(action='SELECT')
                        bpy.ops.pose.paths_clear()
                        bpy.ops.pose.select_all(action='DESELECT')
                        for bo in self.bonelist:
                            o=bpy.context.object
                            b=o.data.bones[bo]
                            b.select=True
                            o.data.bones.active=b        
                            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=lastkey, bake_location='HEADS')
                    #else:
                    #    print ("unchanged")
                    bpy.context.scene["SceneBonelist"] = self.bonelist
            else:
                bpy.context.scene["SceneBonelist"] =["asdasd"]
                print("setting SceneBonelist for first time")
            """
        elif event.type == 'X':  #Delete
            print ("delete")
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action     
            if bpy.context.selected_pose_bones != None:                
                bpy.ops.anim.keyframe_delete()
                
        elif event.type == 'A':  #Move Position Bone this if for personal project
            print("Move Position Bone")
            pointtest = False 
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action     
            
            for bones in obj.pose.bones:
                if "\"_Position\"" in str(bones): #check if bone exists
                    bones.matrix.translation = bpy.context.selected_pose_bones[0].matrix.translation
                    #bones.location[1] = 0
        elif event.type == 'MIDDLEMOUSE' and event.value == "RELEASE":  # Create or Move and Delete Keyframe based on starting position
            print("mmb")
            pointtest = False 
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action     
            if bpy.context.selected_pose_bones != None:  
                if bpy.context.selected_pose_bones.count != 0:
                    for selbone in bpy.context.selected_pose_bones:
                        for f in bpy.data.actions[action.name].fcurves:                       
                            b = (str(f.data_path))
                            if ("\""+selbone.name+"\"") in b:
                                for k in f.keyframe_points:                                
                                    if k.co[0] == bpy.context.scene.frame_current:                                       
                                        k.co[1]= f.evaluate(self.sframe)                     
                                        pointtest = True
                                if pointtest == False:
                                    y=f.evaluate(self.sframe)  
                                    f.keyframe_points.add(1)                
                                    f.keyframe_points[len(f.keyframe_points)-1].co = (bpy.context.scene.frame_current),y                                         
                                f.update()
                endframe = bpy.context.scene.frame_current
                bpy.context.scene.frame_set(self.sframe)
                bpy.ops.anim.keyframe_delete()
                bpy.context.scene.frame_set(endframe)
        elif event.type == 'RIGHTMOUSE':  # Create or Duplicate Keyframe base on starting position                       
            pointtest = False 
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action                       
            if bpy.context.selected_pose_bones != None:  
                if bpy.context.selected_pose_bones.count != 0:    
                    for selbone in bpy.context.selected_pose_bones:
                        for f in bpy.data.actions[action.name].fcurves:                       
                            b = (str(f.data_path))
                            if ("\""+selbone.name+"\"") in b:
                                for k in f.keyframe_points:                                
                                    if k.co[0] == bpy.context.scene.frame_current:                                       
                                        k.co[1]= f.evaluate(self.sframe)                     
                                        pointtest = True
                                if pointtest == False:
                                    y=f.evaluate(self.sframe)  
                                    f.keyframe_points.add(1)                
                                    f.keyframe_points[len(f.keyframe_points)-1].co = (bpy.context.scene.frame_current),y                                         
                                f.update()
        elif event.type == 'W':  # Copy from start to end                      
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action                       
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
            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=bpy.context.scene.frame_end+1, bake_location='HEADS')
                                
        elif event.type == 'R':             # Fix looping  
            print ("trying to fix looping")
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action  
            scn = bpy.context.scene              #current scene
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
                    
            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=bpy.context.scene.frame_end+1, bake_location='HEADS')
            return {'FINISHED'}                        
        elif event.type == 'E':             # Copy and flip animation for selected bone               
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action  
            for selbone in bpy.context.selected_pose_bones:                
                framenumbers=[]
                fcurveindexselbone=[]
                fcurveindexoppobone=[]
                i=0
                ii=0
                copythis=0
                centrebone=False
                #work out opposite bone
                if "_R" in selbone.name:
                    oppobone = str(selbone.name).replace("_R","_L")
                elif "_L" in selbone.name:
                    oppobone = str(selbone.name).replace("_L","_R")
                elif ".L" in selbone.name:
                    oppobone = str(selbone.name).replace(".L",".R")
                elif ".R" in selbone.name:
                    oppobone = str(selbone.name).replace(".R",".L")
                else:
                    oppobone = selbone.name        
                    centrebone = True
                print ("selected bone",selbone.name)
                print ("opposite bone",oppobone)
                #if bone a central bone with no opposite
                if centrebone == True:
                    #if in first half of anim
                    if bpy.context.scene.frame_current < (0.5*bpy.context.scene.frame_end):                     
                        for f in bpy.data.actions[action.name].fcurves:
                            if ('"'+selbone.name+'"') in f.data_path:
                                NumOfKeyframesInFirstHalf = 0
                                NumOfKeyframesInSecondHalf = 0
                                for k in f.keyframe_points:
                                    if k.co[0] < (0.5*bpy.context.scene.frame_end):
                                        NumOfKeyframesInFirstHalf += 1
                                    elif k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                        NumOfKeyframesInSecondHalf += 1               
                                NumOfKeyframes = NumOfKeyframesInSecondHalf + NumOfKeyframesInFirstHalf

                                #remove keyframes from second half of anim
                                while NumOfKeyframesInSecondHalf > 0:
                                    f.keyframe_points.remove(f.keyframe_points[NumOfKeyframes-1])
                                    NumOfKeyframesInSecondHalf -= 1
                                    NumOfKeyframes -= 1                               
                                
                                #copy keyframes from first half to second half
                                i=0
                                for k in f.keyframe_points:
                                    f.keyframe_points.add(1) 
                                    f.keyframe_points[len(f.keyframe_points)-1].co = ((f.keyframe_points[i].co[0])+(0.5*bpy.context.scene.frame_end)),(f.keyframe_points[i].co[1])
                                    f.keyframe_points[len(f.keyframe_points)-1].handle_left_type="AUTO_CLAMPED"
                                    f.keyframe_points[len(f.keyframe_points)-1].handle_right_type="AUTO_CLAMPED"
                                    i += 1

                            #flippose 
                            if ('"'+selbone.name+'"') in f.data_path:               
                                if "location" in f.data_path:
                                   if f.array_index == 0:
                                       for k in f.keyframe_points:
                                           if k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                               k.co[1] =  k.co[1]*-1
                                elif "quat" in f.data_path:
                                    if f.array_index == 2:
                                        for k in f.keyframe_points:
                                            if k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                    elif f.array_index == 3:
                                        for k in f.keyframe_points:
                                            if k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                elif "euler" in f.data_path:
                                    if f.array_index == 2:
                                        for k in f.keyframe_points:
                                            if k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                #finally copy keyframe from start to end
                                f.keyframe_points.add(1)                   
                                f.keyframe_points[len(f.keyframe_points)-1].co = bpy.context.scene.frame_end,f.keyframe_points[0].co[1]
                                f.update()
                    #if in second half of anim
                    if bpy.context.scene.frame_current > (0.5*bpy.context.scene.frame_end):                     
                        for f in bpy.data.actions[action.name].fcurves:
                            if ('"'+selbone.name+'"') in f.data_path:
                                NumOfKeyframesInFirstHalf = 0
                                NumOfKeyframesInSecondHalf = 0
                                for k in f.keyframe_points:
                                    if k.co[0] <= (0.5*bpy.context.scene.frame_end):
                                        NumOfKeyframesInFirstHalf += 1
                                    elif k.co[0] >= (0.5*bpy.context.scene.frame_end):
                                        NumOfKeyframesInSecondHalf += 1               
                                f.update()
                                #remove keyframes from first half of anim
                                while NumOfKeyframesInFirstHalf > 0:
                                    f.keyframe_points.remove(f.keyframe_points[0])
                                    NumOfKeyframesInFirstHalf -= 1    
                                f.update()

                                for k in f.keyframe_points:
                                    f.keyframe_points.insert((k.co[0]-(0.5*bpy.context.scene.frame_end)),k.co[1])
                                f.update()     

                            #flippose 
                            if ('"'+selbone.name+'"') in f.data_path:               
                                if "location" in f.data_path:
                                   if f.array_index == 0:
                                       for k in f.keyframe_points:
                                           if k.co[0] <= (0.5*bpy.context.scene.frame_end):
                                               k.co[1] =  k.co[1]*-1
                                elif "quat" in f.data_path:
                                    if f.array_index == 2:
                                        for k in f.keyframe_points:
                                            if k.co[0] <= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                    elif f.array_index == 3:
                                        for k in f.keyframe_points:
                                            if k.co[0] <= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                elif "euler" in f.data_path:
                                    if f.array_index == 2:
                                        for k in f.keyframe_points:
                                            if k.co[0] <= (0.5*bpy.context.scene.frame_end):
                                                k.co[1] =  k.co[1]*-1
                                #finally copy keyframe from end to start
                                f.keyframe_points.insert(0,1)                   
                                f.keyframe_points[0].co = 0,f.keyframe_points[len(f.keyframe_points)-1].co[1]    
                                f.update()
                    #copy middle frame to end
                    #see if current frame is middle frame 
                    if bpy.context.scene.frame_current == (0.5*bpy.context.scene.frame_end):
                        for f in bpy.data.actions[action.name].fcurves:
                            if ('"'+selbone.name+'"') in f.data_path:
                                #find first or last frame keyframe
                                for k in f.keyframe_points:
                                    if k.co[0] == (0) or  k.co[0] == (bpy.context.scene.frame_end):
                                        #find middle frame keyframe
                                        for k1 in f.keyframe_points:
                                            #copy first or last frame value from middle frame
                                            if k1.co[0] == (0.5*bpy.context.scene.frame_end): 
                                                #flip pose
                                                k.co[1] = k1.co[1]
                                                if "location" in f.data_path:
                                                    if f.array_index == 0:                                                      
                                                        k.co[1] = k1.co[1]*-1
                                                elif "quat" in f.data_path:
                                                    if f.array_index == 2:                                                    
                                                        k.co[1] =  k1.co[1]*-1
                                                    elif f.array_index == 3:
                                                        k.co[1] =  k1.co[1]*-1
                                                elif "euler" in f.data_path:
                                                    if f.array_index == 2:
                                                        k.co[1] =  k1.co[1]*-1
                                            f.update()                   

                elif centrebone == False:
                    #create a list of frames with keys on them
                    for f in bpy.data.actions[action.name].fcurves:    
                        if ('"'+selbone.name+'"') in f.data_path:
                            for p in f.keyframe_points:
                                if p.co[0] not in framenumbers:
                                    framenumbers.append(p.co[0])

                    #create a list of f curve indexs the selected bone uses
                    for f in bpy.data.actions[action.name].fcurves:    
                        if ('"'+selbone.name+'"') in f.data_path:
                            fcurveindexselbone.append(i)                
                        i += 1

                    #create a list of f curve indexs the opposite bone uses
                    for f in bpy.data.actions[action.name].fcurves:    
                        if ('"'+oppobone+'"') in f.data_path:
                            print (oppobone, "  ", f.data_path)
                            fcurveindexoppobone.append(ii)                
                        ii += 1

                    #remove all but 1 keyframes from oppbone side
                    for fc in action.fcurves:  
                        if ('"'+oppobone+'"') not in fc.data_path:
                            continue        
                        while len(fc.keyframe_points) > 1:
                            fc.keyframe_points.remove(fc.keyframe_points[0])
                            
                    #find number of keyframes to add
                    for f in range(len(fcurveindexselbone)):
                        numofkeyframepoitns = (len(action.fcurves[fcurveindexselbone[f]].keyframe_points))
                #        print (numofkeyframepoitns, "in", action.fcurves[fcurveindexselbone[f]].data_path)
                #        print ((len(action.fcurves[fcurveindexoppobone[f]].keyframe_points)), "in", action.fcurves[fcurveindexoppobone[f]].data_path)
                        while len(action.fcurves[fcurveindexoppobone[f]].keyframe_points) < len(action.fcurves[fcurveindexselbone[f]].keyframe_points):         
                            action.fcurves[fcurveindexoppobone[f]].keyframe_points.add()

                    #loop keyframe points on all opposite bone fcruves and grab data from selbone fcruve
                    print ("r1 ", range(len(fcurveindexoppobone)))
                    print ("r2 ", range(len(action.fcurves[fcurveindexselbone[f]].keyframe_points)))
                    print ("r3 ", range(len(action.fcurves[fcurveindexoppobone[f]].keyframe_points)))
                    
                    for f in range(len(fcurveindexoppobone)):
                        print (f)
                        for k in range(len(action.fcurves[fcurveindexselbone[f]].keyframe_points)):
                            print(action.fcurves[fcurveindexselbone[f]].keyframe_points[k].co[0])
                            action.fcurves[fcurveindexoppobone[f]].keyframe_points[k].co = action.fcurves[fcurveindexselbone[f]].keyframe_points[k].co
                            
                    #flippose
                    for f in bpy.data.actions[action.name].fcurves:    
                        if ('"'+oppobone+'"') in f.data_path:
                            if "location" in f.data_path:
                               if f.array_index == 0:
                                   for k in f.keyframe_points:
                                       k.co[1] =  k.co[1]*-1
                            elif "quat" in f.data_path:
                                if f.array_index == 2:
                                    for k in f.keyframe_points:
                                        k.co[1] =  k.co[1]*-1
                                elif f.array_index == 3:
                                    for k in f.keyframe_points:
                                        k.co[1] =  k.co[1]*-1
                            elif "euler" in f.data_path:
                                if f.array_index == 2:
                                    for k in f.keyframe_points:
                                        k.co[1] =  k.co[1]*-1
                    
                    endframe = bpy.context.scene.frame_end
                    startframe  = bpy.context.scene.frame_start-1
                    #offset frames
                    for f in bpy.data.actions[action.name].fcurves:    
                        if ('"'+oppobone+'"') in f.data_path:
                            hm = len(f.keyframe_points)-1
                            for k in f.keyframe_points:
                                k.co[0]=k.co[0]+((endframe-startframe)/2) #offset everything                
                            for k in f.keyframe_points:
                                if k.co[0] == ((endframe-startframe)/2): 
                                    k.co[0]=startframe                   #move mid frame to start, change value later
                                elif k.co[0] > endframe:
                                    k.co[0]= k.co[0]-endframe           #move move overextended frames to start of anim
                            for k in f.keyframe_points:
                                if k.co[0] == endframe:
                                    copythis = k.co[1]
                            for k in f.keyframe_points:
                                if k.co[0] == startframe:
                                    k.co[1]= copythis                    
                        f.update()
                        
            #copy end frame to start
            #see if current frame is end frame                     
            if bpy.context.scene.frame_current == bpy.context.scene.frame_end:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                for f in bpy.data.actions[action.name].fcurves:
                    if ('"'+selbone.name+'"') in f.data_path:
                        #find last keyframe
                        for k in f.keyframe_points:
                            if k.co[0] == (bpy.context.scene.frame_end):
                                #find first keyframe
                                for k1 in f.keyframe_points:
                                    if k1.co[0] == (0): 
                                    #copy last keyframe to first keyframe
                                        k1.co[1] = k.co[1]
                                        print("bbbbbbbbbbbbbbbbbbbbbbbbb")
                                    f.update()
            
            #copy start frame to end
            #see if current frame is start frame 
            if bpy.context.scene.frame_current == (0):
                for f in bpy.data.actions[action.name].fcurves:
                    if ('"'+selbone.name+'"') in f.data_path:
                        #find first keyframe
                        for k in f.keyframe_points:
                            if k.co[0] == (0):
                                #find last keyframe
                                for k1 in f.keyframe_points:                                            
                                    if k1.co[0] == (bpy.context.scene.frame_end): 
                                    #copy first keyframe to last keyframe
                                        k1.co[1] = k.co[1]
                                    f.update()

            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=bpy.context.scene.frame_end+1, bake_location='HEADS')
            return {'FINISHED'}
        elif event.type == 'WHEELUPMOUSE':  # Create or Duplicate Keyframe base on starting position
            keytest = False 
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action
            for selbone in bpy.context.selected_pose_bones:
                for g in action.groups:
                    if selbone.name == g.name: #checks to see if selected bone matches a bone in the action
                        for channel in g.channels :   # channel is fcurve
                            framelist = []
                            for p in channel.keyframe_points :
                                framelist.append(p.co[0]) #making a list of all the keyframes
                                list(framelist)
            for f in range(0,len(framelist)):
                if framelist[f] == bpy.context.scene.frame_current:   
                    bonenextkeyframe = (framelist[f]) #using the keyframe list to find the next keyframe
                    keyindex = f
                    keytest = True                             
            if bpy.context.selected_pose_bones != None and keytest == True:
                if bpy.context.selected_pose_bones.count != 0:                 
                    for selbone in bpy.context.selected_pose_bones:
                        for f in bpy.data.actions[action.name].fcurves:               
                            b = (str(f.data_path))
                            if ("\""+selbone.name+"\"") in b:
                                f.keyframe_points[keyindex-1].co[1] = f.keyframe_points[keyindex].co[1]                                                 
                                f.update()     

        elif event.type == 'WHEELDOWNMOUSE':  # Create or Duplicate Keyframe base on startiong position
            keytest = False 
            obj = bpy.context.object             #active object
            action = obj.animation_data.action   #current action
            for selbone in bpy.context.selected_pose_bones:
                for g in action.groups:
                    if selbone.name == g.name: #checks to see if selected bone matches a bone in the action
                        for channel in g.channels :   # channel is fcurve
                            framelist = []
                            for p in channel.keyframe_points :
                                framelist.append(p.co[0]) #making a list of all the keyframes
            for f in range(0,len(framelist)):
                if framelist[f] == bpy.context.scene.frame_current:   
                    bonenextkeyframe = (framelist[f]) #using the keyframe list to find the next keyframe
                    keyindex = f
                    keytest = True                             
            if bpy.context.selected_pose_bones != None and keytest == True:
                if bpy.context.selected_pose_bones.count != 0:                 
                    for selbone in bpy.context.selected_pose_bones:
                        for f in bpy.data.actions[action.name].fcurves:               
                            b = (str(f.data_path))
                            if ("\""+selbone.name+"\"") in b:
                                f.keyframe_points[keyindex+1].co[1] = f.keyframe_points[keyindex].co[1]                                                 
                                f.update()  
        elif event.type in ('ESC'):  # Cancel
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.sframe = bpy.context.scene.frame_current 
        self.value = event.mouse_x 
        self.dampedvalue = event.mouse_x / 10
        self.looped = 0
        #self.execute(context) #if all executes are uncommented it runs every update
        self.a = bpy.context.object.name 

        #saves matrix from current/start frame
        self.d = {}
        if bpy.context.selected_pose_bones != None:
            for i in range(len(bpy.context.selected_pose_bones)):
               self.d[bpy.context.selected_pose_bones[i].name] = bpy.context.selected_pose_bones[i].matrix.copy() #matrix needs copy or it remains linked            
        print(context.window_manager.modal_handler_add(self))
        return {'RUNNING_MODAL'}
                
def register():
    bpy.utils.register_class(AnimScrubber)


def unregister():
    bpy.utils.unregister_class(AnimScrubber)


if __name__ == "__main__":
    register()