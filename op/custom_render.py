import bpy
import os.path
import random
#########################################所选物体聚焦且充满摄像机
class full(bpy.types.Operator):
    """所选物体聚焦且充满摄像机"""
    bl_idname = "qk.full"
    bl_label = "所选物体充满摄像机"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break
        if "CAMERA" in [obj.type for obj in bpy.data.objects]:
            pass
        else:
            bpy.ops.object.camera_add()
            bpy.ops.view3d.camera_to_view()
        

        bpy.ops.view3d.camera_to_view_selected() #对齐所选到摄像机
        return {"FINISHED"}
#########################################分别渲染合集内所有物体-自动聚焦对象
class collrender(bpy.types.Operator):
    """选择合集，分别自动对焦渲染合集内所有物体"""
    bl_idname = "qk.collrender"
    bl_label = "渲染集合"
    def execute(self, context):
        C = bpy.context
        scn = C.scene
        output_path = scn.render.filepath
        exclude_type = ('LIGHT', 'CAMERA', 'ARMATURE', 'LIGHT_PROBE', 'SPEAKER')

        # 在渲染中禁用所有相关对象
        for b in bpy.data.collections:
            b.hide_render=True   
        bpy.context.collection.hide_render = False
        for ob in C.collection.objects:
            if ob.type not in exclude_type:
                ob.hide_render = True

        for ob in C.collection.objects:
            bpy.data.objects[ob.name].select_set(True)
            bpy.ops.qk.full()
            bpy.data.objects[ob.name].select_set(False)
            if ob.type not in exclude_type:
                # 使对象能够渲染
                ob.hide_render = False
                # 保存路径
                scn.render.filepath = os.path.join(output_path, "{}.jpg".format(ob.name))
                # 调用渲染
                if "CAMERA" in [obj.type for obj in bpy.data.objects]:
                    pass
                else:
                    bpy.ops.object.camera_add()
                    bpy.ops.view3d.camera_to_view()
                bpy.ops.render.render(write_still=True)
                ob.hide_render = True


        # 重置输出路径
        bpy.context.scene.render.filepath = output_path
        # Reset hide_render state
        for ob in C.collection.objects:
            if ob.type not in exclude_type:
                ob.hide_render = False
        
        return {"FINISHED"}

#########################################
class renderlayer(bpy.types.Operator):
    """自动分层渲染到渲染目录，切换到CYCLES,GPU且背景透明"""
    bl_idname = "qk.renderlayer"
    bl_label = "分层渲染"
    def execute(self, context):
        def traverse_tree(t):
            yield t
            for child in t.children:
                yield from traverse_tree(child)
        COLNAME = []
        bpy.context.scene.render.film_transparent = True    #透明背景
        bpy.context.scene.render.engine = 'CYCLES'#CYC渲染器
        bpy.context.scene.cycles.device = 'GPU' #GPU加速
        for col in bpy.data.collections:#获取所有集合名字
            COLNAME.append(col.name)
        layer_coll_master = bpy.context.view_layer.layer_collection
        print(traverse_tree(layer_coll_master))
        for i in range(len(COLNAME)):
            for layer_coll in traverse_tree(layer_coll_master):
                if layer_coll.collection.name == COLNAME[i]:
                    layer_coll.indirect_only = True
        for i in range(len(COLNAME)):
            for layer_coll in traverse_tree(layer_coll_master):
                if layer_coll.collection.name == COLNAME[i]:
                    layer_coll.indirect_only = True
            for layer_coll in traverse_tree(layer_coll_master):
                if layer_coll.collection.name == COLNAME[i]:
                    layer_coll.indirect_only = False
                    #渲染输出
                    scn = bpy.context.scene
                    output_path = scn.render.filepath
                    scn.render.filepath = os.path.join(output_path, "{}.jpg".format(layer_coll.collection.name))
                    bpy.ops.render.render(write_still=True)
                    bpy.context.scene.render.filepath = output_path
                    layer_coll.indirect_only = True
                    break
            


        return {"FINISHED"}
#########################################聚焦并渲染所选对象
class fullrenderselect(bpy.types.Operator):
    """渲染所选对象,ctrl先聚焦后渲染"""
    bl_idname = "qk.fullrenderselect"
    bl_label = "聚焦渲染所选"
    def invoke(self, context,event):
        C = bpy.context
        scn = C.scene
        output_path = scn.render.filepath
        exclude_type = ('LIGHT', 'CAMERA', 'ARMATURE', 'LIGHT_PROBE', 'SPEAKER')

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break
        if event.ctrl == False and event.alt == False and event.shift == False:
            pass
        if event.ctrl:
            bpy.ops.view3d.camera_to_view_selected() #对齐所选到摄像机
        # bpy.ops.view3d.camera_to_view_selected() #对齐所选到摄像机
        b = bpy.context.selected_objects
        # 在渲染中禁用所有相关对象
        for ob in C.collection.objects:
            if ob.type not in exclude_type:
                ob.hide_render = True
        for obj in b:
            if obj.type not in exclude_type:
                # 使对象能够渲染
                obj.hide_render = False
                # 保存路径
        scn.render.filepath = os.path.join(output_path, "{}.jpg".format(obj.name))
            # 调用渲染
        bpy.ops.render.render(write_still=True)
            # 关闭对象可渲染按钮
        for obj in b:
            if obj.type not in exclude_type:
                obj.hide_render = True
        # 重置输出路径
        bpy.context.scene.render.filepath = output_path
        # Reset hide_render state
        for ob in C.collection.objects:
            if ob.type not in exclude_type:
                ob.hide_render = False

        return {"FINISHED"}
class rendersel(bpy.types.Operator):
    """渲染所选摄像机到目录"""
    bl_idname = "qk.rendersel"
    bl_label = "渲染摄像机"

    def execute(self, context):
        scn = bpy.context.scene
        output_path = scn.render.filepath
        objs= bpy.context.selected_objects
        for obj in objs:
            if obj.type == 'CAMERA':
                scn.camera = obj
                scn.render.filepath = os.path.join(output_path, "{}.jpg".format(obj.name))
                bpy.ops.render.render(write_still=True)
                bpy.context.scene.render.filepath = output_path
        return {"FINISHED"}
class renderass(bpy.types.Operator):
    """渲染所选对象到资产"""
    bl_idname = "qk.renderass"
    bl_label = "添加到资产"

    def execute(self, context):
        scene = bpy.context.scene
        exclude_type = ('LIGHT', 'CAMERA', 'ARMATURE', 'LIGHT_PROBE', 'SPEAKER')
        objs = bpy.context.selected_objects
        for obj in objs:
            if obj.type not in exclude_type:
                obj.hide_render = True
                obj.select_set(False)
        for obj in objs:
            if obj.type not in exclude_type:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                print(bpy.context.active_object)
                obj.hide_render = False
                hold_filepath = bpy.context.scene.render.filepath
                switchback = False
                if bpy.ops.view3d.camera_to_view.poll():
                    bpy.ops.view3d.camera_to_view()
                    switchback = True
                previousFileFormat = scene.render.image_settings.file_format
                if scene.render.image_settings.file_format != 'PNG':
                    scene.render.image_settings.file_format = 'PNG'
                filename = str(random.randint(0,100000000000))+".png"
                filepath = str(os.path.abspath(os.path.join(os.sep, 'tmp', filename)))
                bpy.context.scene.render.filepath = filepath
                bpy.ops.view3d.camera_to_view_selected()
                bpy.ops.render.render(write_still = True)
                obj.asset_mark()
                override = bpy.context.copy()
                override['id'] = obj
                bpy.ops.ed.lib_id_load_custom_preview(override,filepath=filepath)
                scene.render.image_settings.file_format = previousFileFormat
                os.unlink(filepath)
                bpy.context.scene.render.filepath = hold_filepath
                obj.hide_render = True
                obj.select_set(False)
                
        for obj in bpy.context.selected_objects:
            if obj.type not in exclude_type:
                obj.hide_render = False
        bpy.ops.file.autopack_toggle()

        return {"FINISHED"}
