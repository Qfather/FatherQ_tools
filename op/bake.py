import bpy
import time
class bake_start(bpy.types.Operator):
    """删除所选所有材质槽及材质球"""
    bl_idname = "qk.bake_start"
    bl_label = "开始烘焙"
    imagetype : bpy.props.EnumProperty(
        name="选择选择种类",
        description="1",
        items=[
            ("0","AO",""),
            ("1","漫射",""),
            ("2","漫射(物体烘焙到物体）",""),
            ("3","所有",""),
        ],
        default  = "0"
        ) 
    dpi : bpy.props.EnumProperty(
        name="选择分辨率",
        description="1",
        items=[
            ("0","256X256",""),
            ("1","512X512",""),
            ("2","1024X1024",""),
            ("3","2048X2048",""),
            ("4","4096X4096","")
        ],
        default  = "2"
        ) 

    def execute(self, context):
        ticks = time.time()
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'
        imagetypelist = ["Ao_","Diffuse_","Diffuse0_","Texture_"] 
        d = self.dpi
        dpilist = [256,512,1024,2048,4096]

        if self.imagetype == "0":
            bpy.context.scene.cycles.bake_type = 'AO'
            bpy.context.scene.render.bake.use_selected_to_active = False
            name = imagetypelist[0]+str(ticks)[5:-8]
            bpy.ops.image.new(name=name,width = dpilist[int(d)],height = dpilist[int(d)],color=(0.5,0.5,0.5,1))
            mat = bpy.data.materials.new(name=name)
            a = bpy.data.images.get(name)
        elif self.imagetype == "1":
            bpy.context.scene.cycles.bake_type = 'DIFFUSE'
            bpy.context.scene.render.bake.use_selected_to_active = False
            name = imagetypelist[1]+str(ticks)[5:-8]
            bpy.ops.image.new(name=name,width = dpilist[int(d)],height = dpilist[int(d)],color=(0.871,0.301,0.012,1))
            mat = bpy.data.materials.new(name=name)
            a = bpy.data.images.get(name)
        elif self.imagetype == "2":
            bpy.context.scene.cycles.bake_type = 'DIFFUSE'
            bpy.context.scene.render.bake.use_selected_to_active = True
            name = imagetypelist[2]+str(ticks)[5:-8]
            bpy.ops.image.new(name=name,width = dpilist[int(d)],height = dpilist[int(d)],color=(1,0,0,1))
            mat = bpy.data.materials.new(name=name)
            a = bpy.data.images.get(name)
        elif self.imagetype == "3":
            bpy.context.scene.cycles.bake_type = 'COMBINED'
            bpy.context.scene.render.bake.use_selected_to_active = False 
            name = imagetypelist[3]+str(ticks)[5:-8]
            bpy.ops.image.new(name=name,width = dpilist[int(d)],height = dpilist[int(d)],color=(0,1,0,1))
            mat = bpy.data.materials.new(name=name)
            a = bpy.data.images.get(name)
        ob = bpy.context.active_object
        if ob.data.materials:
            mat = ob.data.materials[0]
        else:
            ob.data.materials.append(mat)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = nodes.new('ShaderNodeTexImage')
        bsdf = nodes.get("Principled BSDF") 
        nodes.active = node
        node.image = a
        node.location = (-300,300)
        node_tree = mat.node_tree
        # node_tree.links.new(node.outputs[0], bsdf.inputs[0]) 
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"imagetype")
        layout.prop(self,"dpi")
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
