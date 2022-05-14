import bpy
class btb(bpy.types.Operator):
    """在保证骨骼数量与位置对应的前提下，骨骼对齐骨骼，先选A骨骼，再选B骨骼对齐A骨骼"""
    bl_idname = "qk.btb"
    bl_label = "对齐骨骼"
    def execute(self, context):
        objs= bpy.context.selected_objects
        obj = bpy.context.active_object# 获取当前选择的对象
        tobjlist = []             #获取所选其他对象列表
        for o in objs:
            #print(o.select_get)
            if o != obj:
                tobjlist.append(o)
        tobj = tobjlist[0]

        a=[]
        def namelist(obj):
            namelist = []
            for ob in bpy.data.objects[obj.name].pose.bones:
                namelist.append(ob.name)
            return namelist 
        obnlist = namelist(obj)#######所有骨骼名称
        tobnlist = namelist(tobj)   
        def selbone(obj,indx):
            
            bpy.context.object.data.use_mirror_x = False

            arm = bpy.data.objects[obj.name]
            for bone in arm.data.edit_bones:
                if bone.name in namelist(obj)[indx]:
                    bone.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        for i in range(len(obnlist)):
            selbone(obj,i)
            selbone(tobj,i)
            tobjhead = bpy.data.objects[tobj.name].pose.bones[tobnlist[i]].head
            tobjtail = bpy.data.objects[tobj.name].pose.bones[tobnlist[i]].tail
            bpy.data.objects[obj.name].data.edit_bones[obnlist[i]].head = tobjhead
            bpy.data.objects[obj.name].data.edit_bones[obnlist[i]].tail = tobjtail
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}

###################################################
class mir(bpy.types.Operator):
    """添加前缀或者后缀然后对称,然后自动开启对称"""
    bl_idname = "qk.mir"
    bl_label = "对称"
    QZ:bpy.props.StringProperty(name="前缀",default="R_")
    HZ:bpy.props.StringProperty(name="后缀",default="")
    def execute(self, context):
        Q = self.QZ
        H = self.HZ
        boneliset = bpy.context.selected_bones
        for bone in boneliset:
            bone.name = Q+bone.name+H
            print(bone.name)
        bpy.ops.armature.symmetrize()
        bpy.context.object.data.use_mirror_x = True


        return {"FINISHED"}
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)

#########################
class spring(bpy.types.Operator):
    """骨骼编辑模式下选择要做弹簧的骨骼"""
    bl_idname = "qk.spring"
    bl_label = "弹簧"

    def execute(self, context):
        collection = bpy.data.collections.new("非渲染项")
        bpy.context.scene.collection.children.link(collection)


        obj = bpy.context.active_object
        bonename = obj.name
        bonelist = bpy.context.selected_bones
        listname = []
        for bone in bonelist:
            listname.append(bone.name)
            print(bone)
        bonehead = bpy.data.objects[obj.name].pose.bones[bonelist[0].name].head
        bonetail = bpy.data.objects[obj.name].pose.bones[bonelist[0].name].tail
        print(bonehead,bonetail)
        points = []
        mesh = bpy.data.meshes.new(obj.name+"_弹簧跟随")
        points.append(bonehead)
        points.append(bonetail)
        mesh.from_pydata(points,[(0,1)],[])
        obj0 = bpy.data.objects.new(obj.name+"_弹簧跟随",mesh)
        bpy.data.collections["非渲染项"].objects.link(obj0)
        obj0.parent = obj


        v = obj0.data.vertices[0]
        groups0 = obj0.vertex_groups.new(name="0")
        groups0 = obj0.vertex_groups['0']
        groups0.add([0],1,'REPLACE')
        groups0.add([1],0.5,'REPLACE')
        groups1 = obj0.vertex_groups.new(name="1")
        groups1 = obj0.vertex_groups['1']
        groups1.add([1],50,'REPLACE')
        bpy.context.view_layer.objects.active = obj0
        bpy.ops.object.modifier_add(type='CLOTH')
        bpy.context.object.modifiers[-1].settings.time_scale = 0.75
        bpy.context.object.modifiers[-1].settings.vertex_group_mass = "0"
        c = obj.pose.bones
        poselist = []
        for b in c:
            if b.name in listname:
                poselist.append(b)
                
        for i in range(len(poselist)):
            if i == 0:
                poselist[i].constraints.new('DAMPED_TRACK')
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].target = bpy.data.objects[obj0.name]
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].subtarget = "1"
            else:
                poselist[i].constraints.new('COPY_ROTATION')
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].target = bpy.data.objects[bonename]
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].subtarget = poselist[i-1].name
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].target_space = 'LOCAL'
                bpy.context.object.pose.bones[poselist[i].name].constraints[-1].owner_space = 'LOCAL'



        return {"FINISHED"}