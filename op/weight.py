import bpy
import numpy as np
from bpy.types import Menu
# ########################################开始权重！
class wset(bpy.types.Operator):
    """个人习惯权重前设置"""
    bl_idname = "qk.wset"
    bl_label = "开始权重"
    def execute(self, context):
        bpy.context.scene.tool_settings.vertex_group_user = 'ACTIVE'
        bpy.context.scene.tool_settings.use_auto_normalize = True
        return {"FINISHED"}

#########################################对齐不同物体多个分别单个顶点的权重
class wei_point(bpy.types.Operator):
    """对齐不同物体多个分别单个顶点的权重"""
    bl_idname = "qk.wei_point"
    bl_label = "对齐权重"
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')# 进入对象模式更新选定的顶点
        objs= bpy.context.selected_objects
        obj = bpy.context.active_object# 获取当前选择的对象
        tobjlist = []             #获取所选其他对象列表
        for o in objs:
            print(o.select_get)
            if o != obj:
                tobjlist.append(o)

        def indexn (obje):########获取所选点索引列表函数
            sel = np.zeros(len(obje.data.vertices), dtype=np.bool)# 为每个顶点创建一个空值的numpy数组
            obje.data.vertices.foreach_get('select', sel)
            c=np.sum(sel==True)#所选点数量
            obje.data.vertices.foreach_get('select', sel)# 如果顶点被选中，用True/False填充数组
            for ind in np.where(sel==True)[0]:# 循环遍历当前选择的每个顶点
                v = obje.data.vertices[ind]
                #print('Vertex {} at position {} is selected'.format(v.index, v.co))
                vindex  = v.index
                # 如果你只想要第一个，你可以直接打断这里
                break
            return vindex

        def weiname(ob,ind): #####对象，顶点索引所拥有的顶点组的名字列表
            
            assert ob is not None and ob.type == 'MESH', "active object invalid"
            # ensure we got the latest assignments and weights
            ob.update_from_editmode()
            me = ob.data
            # create vertex group lookup dictionary for names
            vgroup_names = {vgroup.index: vgroup.name for vgroup in ob.vertex_groups}

            # create dictionary of vertex group assignments per vertex
            vgroups = {v.index: [vgroup_names[g.group] for g in v.groups] for v in me.vertices}
            vgroupslist = vgroups[ind]
            return vgroupslist

        gro = bpy.context.object.vertex_groups############该对象顶点组所有列表
        objindex = indexn(obj) #获取活动对象点索引列表
        objwiglist = weiname(obj,objindex)#获取活动对象点索引列表的名字
        objwvalue = [] #对象点索引的值
        for w in objwiglist:
            objwvalue.append(gro[w].weight(objindex))
            print(str(w),gro[w].weight(objindex))

        for t in tobjlist:
            c = indexn(t) #获取要赋予物体点索引
            tobjname = weiname(t,c) #获取要赋予物体的顶点组列表名字 
            for a in tobjname:
                if a in objwiglist:
                    t.vertex_groups[a].add([c],objwvalue[objwiglist.index(a)],'REPLACE' )
                else:
                    t.vertex_groups[a].remove([c])
        
        bpy.ops.object.mode_set(mode='EDIT')
        return {"FINISHED"}
#########################################清空所选顶点组
class rmpg(bpy.types.Operator):
    """清空所选顶点组"""
    bl_idname = "qk.rmpg"
    bl_label = "清空顶点组"
    def execute(self, context):
        objs= bpy.context.selected_objects
        for obj in objs:
            bpy.context.view_layer.objects.active = obj
            if len(obj.vertex_groups) >= 1:
                bpy.ops.object.vertex_group_remove(all=True)

        return {"FINISHED"}

#########################################传递权重
class hwe(bpy.types.Operator):
    """有权重的模型放骨骼下子集第一个"""
    bl_idname = "qk.hwe"
    bl_label = "传递权重"
    def execute(self, context):
        objs= bpy.context.selected_objects
        objlist = []
        for obj in objs:
            if obj.type == "ARMATURE":
                bone = obj
            else:
                objlist.append(obj)
        obj = objlist[0]
        objlist = objlist[1:]
        for obj in objlist:
            obj.select_set(False)
        for obj in objlist:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            bpy.ops.object.data_transfer(use_reverse_transfer=True, use_freeze=False, data_type='VGROUP_WEIGHTS', vert_mapping='POLYINTERP_NEAREST', layers_select_src='NAME', layers_select_dst='ALL')
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)
            print('完成'+obj.name+'权重传递')

        return {"FINISHED"}
#########################################权重笔刷相加
class wbrush_add(bpy.types.Operator):
    """权重笔刷模式改为相加"""
    bl_idname = "qk.wbrushadd"
    bl_label = "相加"
    def execute(self, context):
        bpy.data.brushes["Draw"].blend = 'ADD'

        return {"FINISHED"}
#########################################权重笔刷相减
class wbrush_sub(bpy.types.Operator):
    """权重笔刷模式改为相减"""
    bl_idname = "qk.wbrushsub"
    bl_label = "相减"
    def execute(self, context):
        bpy.data.brushes["Draw"].blend = 'SUB'

        return {"FINISHED"}
class wbrush_blur(bpy.types.Operator):
    """模糊"""
    bl_idname = "qk.wbrushblur"
    bl_label = "模糊"
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Blur")
        return {"FINISHED"}
class wbrush_gra(bpy.types.Operator):
    """渐变"""
    bl_idname = "qk.wbrushgra"
    bl_label = "渐变"
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.gradient")
        return {"FINISHED"}




########################
class repoint(bpy.types.Operator):
    """删除权重为0的顶点组,会自动识别镜像保留镜像顶点组"""
    bl_idname = "qk.repoint"
    bl_label = "清理顶点组"
    num:bpy.props.IntProperty(name= "忽略前缀命名",default=2)
    num0:bpy.props.IntProperty(name= "忽略后缀命名",default=0)
    def execute(self, context):
        f = self.num
        b = self.num0
        def survey(obj):
            maxWeight = {}
            for i in obj.vertex_groups:
                maxWeight[i.index] = 0

            for v in obj.data.vertices:
                for g in v.groups:
                    gn = g.group
                    w = obj.vertex_groups[g.group].weight(v.index)
                    if (maxWeight.get(gn) is None or w>maxWeight[gn]):
                        maxWeight[gn] = w
            return maxWeight
        obj = bpy.context.active_object

        gl = [group.name for group in obj.vertex_groups]
        print(gl)
        maxWeight = survey(obj)
        ka = []
        ka.extend(maxWeight.keys())
        ka.sort(key=lambda gn: -gn)
        print (ka)
        l = []
        for gn in ka:
            if maxWeight[gn] > 0 :
                l.append(obj.vertex_groups[gn].name[f-1:-b])
        print(l)
        for gn in ka:
            if maxWeight[gn] <= 0 :
                if 'MIRROR' in [m.type for m in bpy.context.active_object.modifiers]:
                    if obj.vertex_groups[gn].name[:-2] not in l:
                        obj.vertex_groups.remove(obj.vertex_groups[gn])
                else:
                    obj.vertex_groups.remove(obj.vertex_groups[gn])  

        return {"FINISHED"}
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)