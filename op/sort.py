import bpy
import random
def ShowMessageBox(message = "", title = "提示", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
class collrandom(bpy.types.Operator):
    """所有集合随机排列组合"""
    bl_idname = "qk.collrandom"
    bl_label = "所有集合排组"
    def execute(self, context):
        COLNAME = []
        for col in bpy.data.collections:
            COLNAME.append(col.name)
        textlist = []
        for i in range(len(COLNAME)):
            alist = []
            for a in bpy.data.collections[COLNAME[i]].all_objects:
                alist.append(a)
                a.hide_set(True)
                a.hide_render = True
            rn = random.randint(0, len(bpy.data.collections[COLNAME[i]].all_objects)-1)
            textlist.append(COLNAME[i]+':'+str(rn))
            for b in range(len(bpy.data.collections[COLNAME[i]].all_objects)):
                if rn == b:
                    alist[b].hide_set(False)
                    alist[b].hide_render = False
        mess = ""
        for text in textlist:
            mess += text+"   "
        ShowMessageBox(mess)
        return {"FINISHED"}

#########################################所选子集随机排列组合
class rand_sel(bpy.types.Operator):
    """所选子集随机排列组合"""
    bl_idname = "qk.rand_sel"
    bl_label = "所选子集排组"
    def execute(self, context):
        
        objs = bpy.context.selected_objects
        print(objs)
        textlist = []
        for i in range(len(objs)):
            alist = []
            for c in objs[i].children:
                alist.append(c)

            for a in objs[i].children_recursive:
                a.hide_set(True)
                a.hide_render = True
            rn = random.randint(0, len(objs[i].children)-1)
            print(objs[i].name+':'+str(rn))
            textlist.append(objs[i].name+':'+str(rn))
            for b in range(len(objs[i].children)):
                if rn == b:
                    alist[b].hide_set(False)
                    alist[b].hide_render = False
                    for obj in alist[b].children_recursive:
                        obj.hide_set(False)
                        obj.hide_render = False
        return {"FINISHED"}