import bpy
import time
class XCR(bpy.types.Operator):
    """处理香肠人组合"""
    bl_idname = "qk.xcr"
    bl_label = "清理香肠人"
    def execute(self, context):
        objs = bpy.context.selected_objects
        nlist = ["脸颊","眼睛","嘴巴","衣服","bone"]
        a = bpy.data.objects['衣服'].children
        print(a)
        blist = []
        for obj in objs:
            if obj.name in nlist:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.ops.object.delete()
            else:
                blist.append(obj) 

        print(blist)
        for obj in blist :
            obj.select_set(True)
        bpy.context.view_layer.objects.active = a[0]
        a[0].select_set(True)


        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        try:
            
            bpy.ops.machin3.clean_up()
        except:
            bpy.ops.object.mode_set(mode='OBJECT')
        ticks = time.time()
        bpy.context.active_object.name = "香肠人编号_"+ str(ticks)[5:-8]
        return {"FINISHED"}