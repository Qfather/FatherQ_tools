import bpy
class sk_start(bpy.types.Operator):
    """开始并添加形态建"""
    bl_idname = "qk.sk_start"
    bl_label = "开始形态"
    def execute(self, context):
        op = bpy.context.active_object
        op.shape_key_add(name = "基础形态",from_mix=False)
        op.shape_key_add(name = "变形形态",from_mix=True)
        bpy.context.object.active_shape_key_index = 1
        op.active_shape_key.value = 1
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Grab")
        return {"FINISHED"}

class sk_add(bpy.types.Operator):
    """添加新形态建"""
    bl_idname = "qk.sk_add"
    bl_label = "增加形态"
    def execute(self, context):
        op = bpy.context.active_object
        opindex = op.active_shape_key_index
        op.active_shape_key.value = 0
        op.shape_key_add(name = "变形形态"+"_"+str(opindex+1),from_mix=False)
        bpy.context.object.active_shape_key_index = opindex+1
        op.active_shape_key.value = 1
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Grab")
        return {"FINISHED"}

class sk_mir(bpy.types.Operator):
    """镜像当前形态"""
    bl_idname = "qk.sk_mir"
    bl_label = "镜像形态"
    def execute(self, context):
        op = bpy.context.active_object
        opindex = op.active_shape_key_index
        op.shape_key_add(name = "变形形态"+"_"+str(opindex+1),from_mix=True)
        bpy.context.object.active_shape_key_index = opindex+1
        bpy.ops.object.shape_key_mirror(use_topology=False)
        bpy.context.object.active_shape_key_index = opindex
        op.active_shape_key.value = 0
        bpy.context.object.active_shape_key_index = opindex+1
        op.active_shape_key.value = 1
        return {"FINISHED"}