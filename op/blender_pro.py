import bpy
import os.path
from mathutils import Matrix, Vector
import numpy as np
import random
class EportFBX(bpy.types.Operator):
    """一键导出FBX到自身路径"""
    bl_idname = "qk.portfbx"
    bl_label = "一键导出FBX"
    def execute(self, context):
        file0 = os.path.dirname(bpy.data.filepath)
        name = bpy.path.basename(bpy.context.blend_data.filepath)
        obj =  bpy.context.active_object
        bpy.ops.export_scene.fbx(
            filepath=bpy.path.abspath((file0+"\\"+"Auto-"+name[:-6]+"-"+obj.name)+".fbx"),
            use_selection=True,
            path_mode='COPY',
            embed_textures=True

            )
        return {"FINISHED"}
#########################################全部显示
class view_render(bpy.types.Operator):
    """显示渲染所有对象"""
    bl_idname = "qk.view_render"
    bl_label = "显示/渲染所有对象"
    def execute(self, context):
        for obj in bpy.data.objects:
            obj.hide_set(False)
            obj.hide_render = False
        return {"FINISHED"}


########################################原点到几何体下方中心
class bottomcenter(bpy.types.Operator):
    """原点到几何体下方中心"""
    bl_idname = "qk.bottomcenter"
    bl_label = "原点至中心下方"

    def execute(self, context):
        def origin_to_bottom(ob, matrix=Matrix()):
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)#应用旋转缩放
            me = ob.data
            mw = ob.matrix_world
            local_verts = [matrix @ Vector(v[:]) for v in ob.bound_box]
            o = sum(local_verts, Vector()) / 8
            o.z = min(v.z for v in local_verts)
            o = matrix.inverted() @ o
            me.transform(Matrix.Translation(-o))

            mw.translation = mw @ o

        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                origin_to_bottom(o)
                #origin_to_bottom(o, matrix=o.matrix_world) # global
        return {"FINISHED"}
#########################################添加资产摄像机
class acamera(bpy.types.Operator):
    """创建一个摄像机45度角对着世界中心，设置分辨率为256*256，背景透明"""
    bl_idname = "qk.acamera"
    bl_label = "资产相机"

    def execute(self, context):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(2, -2, 2), rotation=(np.deg2rad(55), 0, np.deg2rad(45)), scale=(1, 1, 1))
        bpy.context.scene.render.resolution_x = 256
        bpy.context.scene.render.resolution_y = 256
        bpy.context.scene.render.film_transparent = True
        return {"FINISHED"}

class pmove(bpy.types.Operator):
    """队列移动旋转缩放"""
    bl_idname = "qk.pmove"
    bl_label = "队列"
    buer:bpy.props.BoolProperty(name="索引翻转",default= False)
    ran:bpy.props.BoolProperty(name="随机排序",default= False)
    juli:bpy.props.FloatVectorProperty(name= "距离",default=(0,0,0))
    rong:bpy.props.FloatVectorProperty(name= "旋转",default=(0,0,0))
    suofangA:bpy.props.FloatProperty(name= "整体缩放",default=1)
    suofang:bpy.props.FloatVectorProperty(name= "缩放",default=(1,1,1))
    def execute(self, context):
        t = self.juli
        s = self.suofangA
        sm = self.suofang
        r = self.rong
        b = self.buer
        ra = self.ran
        objs = bpy.context.selected_objects
        if b == True:
            objs = list(reversed(objs))
        if ra == True:
            random.shuffle(objs) 
        print(s)
        for obj in objs:
            for i in range(len(t)):
                # if t[i] != 0:
                obj.location[i] = t[i]*objs.index(obj)
            if s != 1:
                print("333")
                obj.scale[0] = obj.scale[1] = obj.scale[2] =s*(objs.index(obj)+1)
            else:
                if sm[0] != 1:

                    obj.scale[1] = obj.scale[2] = sm[0]*(objs.index(obj)+1)
                    print(obj.name)
                    print(obj.scale[1])
                    print(sm[0]*(objs.index(obj)+1))
                    print(obj.scale[2])
                    print("111111111")
                else:
                    print("222")
                    obj.scale[1] = obj.scale[2] = 1
                if sm[1] != 1:
                    obj.scale[0] = obj.scale[2] = sm[1]*(objs.index(obj)+1)
                else:
                    obj.scale[0] = obj.scale[2] = 1
                if sm[2] != 1:
                    obj.scale[0] = obj.scale[1] = sm[2]*(objs.index(obj)+1)
                else:
                    obj.scale[0] = obj.scale[1] = 1
            for e in range(len(r)):
                obj.rotation_euler[e] = np.deg2rad(r[e]*objs.index(obj))
                    
            
            

        return {"FINISHED"}
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
#########################################点控制脚本
class pointcon(bpy.types.Operator):
    """给所选点创建控制点"""
    bl_idname = "qk.pointcon"
    bl_label = "创建点控制器"
    def execute(self, context):
        mode = bpy.context.active_object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = bpy.context.object
        sel = np.zeros(len(obj.data.vertices), dtype=np.bool)
        obj.data.vertices.foreach_get('select', sel)
        c=np.sum(sel==True)
        grouplist = []
        namelist = []
        for i in range(c):
            hook = bpy.ops.object.modifier_add(type='HOOK')
            group = obj.vertex_groups.new( name ='控制点'+str(i) )
            group = obj.vertex_groups['控制点'+str(i) ]
            namelist.append('控制点'+str(i)) 
            grouplist.append(group)
        hooks = []
        print(namelist)
        for modifier in obj.modifiers:
            hooks.append(modifier)

        #print(hooks)
        # Populate the array with True/False if the vertex is selected
        null = []
        indx = [] 
        for ind in np.where(sel==True)[0]:
            # Loop over each currently selected vertex
            v = obj.data.vertices[ind]
            bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=v.co, scale=(1, 1, 1))
            bpy.context.active_object.name = '控制点'
            bpy.context.active_object.empty_display_size = 0.2
            bpy.context.active_object.parent = obj

            null.append(bpy.context.active_object)
            print('Vertex {} at position {} is selected'.format(v.index, v.co))
            indx.append(v.index)
            # If you just want the first one you can break directly here
            # break
        #print(indx)
        #print(null)
        for i in range(c):
            grouplist[i].add([indx[i]], 100, 'REPLACE' )
            hooks[i].object = null[i]
            hooks[i].vertex_group = namelist[i]


#bpy.ops.object.mode_set(mode=mode)
# Go back to the previous mode
        return {"FINISHED"}
#########################################开关编辑模式显示罩体
class boneedit(bpy.types.Operator):
    """开关所选对象修改器的所有编辑模式与遮罩模式"""
    bl_idname = "qk.boneedit"
    bl_label = "骨骼编辑显示"
    def execute(self, context):
        objs= bpy.context.selected_objects
        for obj in objs:
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE':
                    modifier.show_in_editmode = True
                    modifier.show_on_cage = True
        return {"FINISHED"}
class automir(bpy.types.Operator):
    """自动删除+x的点然后镜像，点控制在-0.01到0.01可以自动"""
    bl_idname = "qk.automir"
    bl_label = "自动镜像"
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT') 
        for polygon in bpy.context.active_object.data.polygons:
            polygon.select = False
        for edge in bpy.context.active_object.data.edges:
            edge.select = False
        for vertex in bpy.context.active_object.data.vertices:
            vertex.select = False
            if vertex.co.x> -0.01 and vertex.co.x< 0.01:
                vertex.co.x = 0 
            if vertex.co.x > 0.00000001:
                vertex.select = True
            
        bpy.ops.object.mode_set(mode='EDIT') 
        bpy.ops.mesh.delete(type='VERT')
        try:
            bpy.ops.machin3.clean_up()
        except:
            pass
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_add(type='MIRROR')
        return {"FINISHED"}
class plFBX(bpy.types.Operator):
    """批量导出FBX到自身路径"""
    bl_idname = "qk.plfbx"
    bl_label = "批量导出FBX"
    num:bpy.props.IntProperty(name= "输出个数",default=1)
    def execute(self, context):
        n = self.num
        for e in range(n):
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
                textlist.append(objs[i].name+':'+str(rn))
                for b in range(len(objs[i].children)):
                    if rn == b:
                        alist[b].hide_set(False)
                        alist[b].hide_render = False
                        for obj in alist[b].children_recursive:
                            obj.hide_set(False)
                            obj.hide_render = False
            for obj in bpy.data.objects:
                print(obj.hide_get())
                if obj.hide_get() == False:    
                    obj.select_set(True)
                    if obj in objs:
                        obj.select_set(False)

            #导出所选
            file0 = os.path.dirname(bpy.data.filepath)
            name = bpy.path.basename(bpy.context.blend_data.filepath)
            bpy.ops.export_scene.fbx(
                filepath=bpy.path.abspath((file0+"\\"+"批量-"+name[:-6]+"-")+str(e+1)+".fbx"),
                use_selection=True,
                path_mode='COPY',
                embed_textures=True

                )
            for obj in bpy.data.objects:
                obj.select_set(False)
            for obj in objs:
                obj.select_set(True)
        return {"FINISHED"}
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
class blfbx(bpy.types.Operator):
    """批量导出FBX，ctrl同时打包贴图"""
    bl_idname = "qk.blfbx"
    bl_label = "批量导出FBX"
    def invoke(self, context, event):
        file0 = os.path.dirname(bpy.data.filepath)
        objs= bpy.context.selected_objects
        for obj in objs:
            obj.select_set(False)
        conlist = []
        for con in bpy.data.collections:
            for obj in con.objects:
                if obj in objs:
                    try:
                        os.makedirs(file0+"\\"+con.name)
                    except:
                        pass  
        for obj in objs:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            print("1111")
            if event.ctrl == False and event.alt == False and event.shift == False:
                try:
                    bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath((file0+"\\"+obj.users_collection[0].name+"\\"+obj.name)+".fbx"),
                    use_selection=True,
                    )
                except:
                    bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath((file0+"\\"+obj.name)+".fbx"),
                    use_selection=True,
                    )
            if event.ctrl:
                try:
                    bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath((file0+"\\"+obj.users_collection[0].name+"\\"+obj.name)+".fbx"),
                    use_selection=True,
                    path_mode='COPY',
                    embed_textures=True
                    )
                except:
                    bpy.ops.export_scene.fbx(
                    filepath=bpy.path.abspath((file0+"\\"+obj.name)+".fbx"),
                    use_selection=True,
                    path_mode='COPY',
                    embed_textures=True
                    )
            obj.select_set(False)
        return {"FINISHED"}
