import bpy
import os
from PIL import Image
def ShowMessageBox(message = "", title = "提示", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
class tyname(bpy.types.Operator):
    """替换所选名称材质名-对象名"""
    bl_idname = "qk.tyname"
    bl_label = "统一命名"
    benti : bpy.props.EnumProperty(
        name="",
        description="1",
        items=[
            ("0","对象名变成材质名",""),
            ("1","材质名变成对象名",""),
        ]
    ) 
    def execute(self, context):
        b = bpy.context.selected_objects
        if self.benti == "0" :
            for obj in b:
                c = obj.active_material
                if c:
                    obj.name = c.name
                else:
                    ShowMessageBox(message = "首先你要有个材质", title = "提示", icon = 'INFO')
        elif self.benti == "1":
            for obj in b:
                name = obj.name
                c = obj.active_material
                if c:
                    c.name = name
                else:
                    ShowMessageBox(message = "首先你要有个材质", title = "提示", icon = 'INFO')
        
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"benti")
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)


#########################################批量索引后缀
class num(bpy.types.Operator):
    """以活动对象为基础批量命名并加后缀"""
    bl_idname = "qk.num"
    bl_label = "NUM"
    def execute(self, context):
        objs= bpy.context.selected_objects
        op = bpy.context.active_object
        objname = op.name
        for obj in objs:
            obj.name = objname+"_"+str(objs.index(obj))
            print(obj.name)
        return {"FINISHED"}

class refile(bpy.types.Operator):
    """更改图片文件名为材质名+输入端口"""
    bl_idname = "qk.refile"
    bl_label = "改图名"
    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=False, do_recursive=True)
        for mat in bpy.data.materials:
            l = mat.node_tree.nodes["Principled BSDF"].inputs
            for a in l:
                print(a.name)
                if a.links:
                    if a.links[0].from_node.type == "TEX_IMAGE":
                        a.links[0].from_node.image.name = mat.name+"_"+a.name
                        print(a.links[0].from_node.image.name)
                    else:
                        a.links[0].from_node.inputs[1].links[0].from_node.image.name = mat.name+"_"+a.name
        for image in bpy.data.images:
            a = image.filepath_from_user()
            im = Image.open(a)
            print(im)
            c = a.split("\\")[-1]
            file = a[:-len(c)]
            newname = file+image.name+".png"
            im.close()
            os.rename(a,newname)
        return {"FINISHED"}
