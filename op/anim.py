import bpy
class offsetkf(bpy.types.Operator):
    """清空所选顶点组"""
    bl_idname = "qk.offsetkf"
    bl_label = "偏移子关节动画"
    oset:bpy.props.IntProperty(name= "偏移帧数",default=0)
    def execute(self, context):
        o = self.oset
        action = bpy.data.actions[0]
        list0 = []
        for fcu in action.fcurves:
            print(fcu.data_path + " channel " + str(fcu.array_index))
            list0.append(fcu)
            
        print(list0)
        bonename = []
        for bone in bpy.context.object.pose.bones:
            bonename.append(bone.name)
        for i in range(len(list0)):
            for keyframe in list0[i].keyframe_points:
                keyframe.co[0] += (o*int(i/2))
        return {"FINISHED"}
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)