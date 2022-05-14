import bpy
import random
import os.path
#########################################批量索引后缀
def ShowMessageBox(message = "", title = "提示", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
class removemat(bpy.types.Operator):
    """删除所选所有材质槽及材质球"""
    bl_idname = "qk.removemat"
    bl_label = "删除所有材质"
    def execute(self, context):
        objs = bpy.context.selected_objects
        for obj in objs:
            bpy.context.view_layer.objects.active = obj
            a = obj.material_slots
            for x in range(len(a)): 
                obj.active_material_index = 0 
                bpy.ops.object.material_slot_remove() 
        return {"FINISHED"}
class sp_base_mat(bpy.types.Operator):
    """为所有对象添加一个基础材质以供SP使用"""
    bl_idname = "qk.sp_base_mat"
    bl_label = "批量SP材质"
    def execute(self, context):
        objs= bpy.context.selected_objects
        bpy.ops.qk.removemat
        for obj in objs:

            mat = bpy.data.materials.get(obj.name)
            if mat is None:
                # create material
                mat = bpy.data.materials.new(name=obj.name)
            # Assign it to object
            mat.diffuse_color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),1)
            if obj.data.materials:
                # assign to 1st material slot
                obj.data.materials[0] = mat
            
            else:
                # no slots
                obj.data.materials.append(mat)
        file0 = os.path.dirname(bpy.data.filepath)
        name = bpy.path.basename(bpy.context.blend_data.filepath)
        bpy.ops.export_scene.fbx(
            filepath=bpy.path.abspath((file0+"\\"+"SP-"+name[:-6])+".fbx"),
            use_selection=True,
            path_mode='COPY',
            embed_textures=True

            )
        return {"FINISHED"}
class ctoutline(bpy.types.Operator):
    """给物体添加卡通描边"""
    bl_idname = "qk.ctoutline"
    bl_label = "卡通描边"
    type0 : bpy.props.EnumProperty(
        name="选择选择种类",
        description="1",
        items=[
            ("0","较细-一半用于角色",""),
            ("1","较粗-一半用于物品",""),
        ],
        default  = "0"
        ) 
    def execute(self, context):
        t = self.type0
        tlist = [800,100]
        try:
            obj = bpy.context.active_object
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers[-1].use_flip_normals = True
            di = obj.dimensions
            sa = -(di[0]+di[1]+di[2])/3/tlist[int(t)]
            bpy.context.object.modifiers[-1].thickness = sa
            bpy.context.object.modifiers[-1].offset = 1
            #新建材质
            name = obj.name+'_描边'
            mat = bpy.data.materials.new(name=name)
            obj.data.materials.append(mat)
            obj.active_material_index = len(obj.material_slots) - 1
            bpy.context.object.active_material.use_backface_culling = True
            a = obj.active_material_index
            print(a)
            bpy.context.object.modifiers[-1].material_offset = int(a)
            #节点
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            mat.node_tree.nodes.clear()
            node = nodes.new('ShaderNodeEmission')
            output = nodes.new(type = 'ShaderNodeOutputMaterial')
            output.location = (-100,300)
            node.inputs[0].default_value = (0,0,0,1)
            node.location = (-300,300)
            node_tree = mat.node_tree
            node_tree.links.new(node.outputs[0],output.inputs['Surface']) 
        except:
            ShowMessageBox(message = "请选择一个对象", title = "提示", icon = 'INFO')
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"type0")
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
        
class basect(bpy.types.Operator):
    """平滑着色后添加基础卡通材质"""
    bl_idname = "qk.basect"
    bl_label = "基础卡通材质"
    a:bpy.props.FloatVectorProperty(  
                                    name="颜色",
                                    subtype='COLOR',
                                    default=(1.0, 1.0, 1.0),
                                    min=0.0, max=1.0,
                                    description="color picker"
                                    )
    blur:bpy.props.BoolProperty(
        name="边缘模糊"
    )
    def execute(self, context):
        bpy.ops.qk.removemat()
        obj = bpy.context.active_object
        col = self.a 
        print(col)
        try:
            bpy.ops.object.shade_smooth()
            name = obj.name+'_卡通材质'
            mat = bpy.data.materials.new(name=name)
            obj.data.materials.append(mat)
            obj.active_material_index = len(obj.material_slots) - 1
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            mat.node_tree.nodes.clear()
            diff = nodes.new('ShaderNodeBsdfDiffuse')
            diff.location = (0,0)
            srgb = nodes.new('ShaderNodeShaderToRGB')
            srgb.location = (200,0)
            math = nodes.new('ShaderNodeMath')
            math.operation = "POWER"
            math.location = (400,0)
            colorramp = nodes.new('ShaderNodeValToRGB')
            colorramp.location = (600,0)
            if self.blur == False:
                colorramp.color_ramp.interpolation = 'CONSTANT'
            else:
                colorramp.color_ramp.interpolation = 'LINEAR'
            colorramp.color_ramp.elements[0].color = (0.1,0.1,0.1,1)
            colorramp.color_ramp.elements[0].position = (0.6)
            colorramp.color_ramp.elements[1].color = (0.4,0.4,0.4,1)
            colorramp.color_ramp.elements[1].position = (0.63)
            colorramp.color_ramp.elements.new(0.780)
            colorramp.color_ramp.elements[2].color = (0.4,0.4,0.4,1)
            colorramp.color_ramp.elements.new(0.80)
            colorramp.color_ramp.elements[3].color = (1,1,1,1)
            rgb = nodes.new('ShaderNodeRGB')
            rgb.location = (600,300)
            rgb.outputs[0].default_value = (col[0],col[1],col[2],1)
            math0 = nodes.new('ShaderNodeMixRGB')
            math0.blend_type = "MULTIPLY"
            math0.inputs[0].default_value = 1
            math0.location = (1000,0)
            output = nodes.new(type = 'ShaderNodeOutputMaterial')
            output.location = (1200,0)
            node_tree = mat.node_tree
            node_tree.links.new(diff.outputs[0],srgb.inputs[0]) 
            node_tree.links.new(srgb.outputs[0],math.inputs[0]) 
            node_tree.links.new(math.outputs[0],colorramp.inputs[0]) 
            node_tree.links.new(rgb.outputs[0],math0.inputs[1]) 
            node_tree.links.new(colorramp.outputs[0],math0.inputs[2]) 
            node_tree.links.new(math0.outputs[0],output.inputs[0]) 
        except:
            ShowMessageBox(message = "请选择一个对象", title = "提示", icon = 'INFO')
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"a")
        layout.prop(self,"blur")
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
class textokt(bpy.types.Operator):
    """把贴图材质转换为卡通材质,直接为常值过度，ctrl为线性过度"""
    bl_idname = "qk.textokt"
    bl_label = "贴图转卡通"
    def invoke(self,context,event):
        obj = bpy.context.active_object
        matlist = []
        for mat in obj.material_slots:
            matlist.append(mat)
        print(matlist)
        for i in range(len(matlist)):
            matname = matlist[i].name
            mat = bpy.data.materials[matname]
            nodes = mat.node_tree.nodes
            bsdf = nodes.get("Principled BSDF")
            ceshilist = []
            for node in nodes:
                if node.bl_idname == "ShaderNodeTexImage":
                    ceshilist.append(node)
            if len(ceshilist)>0:
                a = bsdf.inputs[0].links[0].from_node
                print(a.bl_idname)
                if a.bl_idname == "ShaderNodeMixRGB":
                    a = a.inputs[1].links[0].from_node
                for node in nodes:
                    if node != a and node.bl_idname != 'ShaderNodeOutputMaterial':
                        nodes.remove(node) 
            else:
                for node in nodes:
                    if node.bl_idname != 'ShaderNodeTexImage' and node.bl_idname != 'ShaderNodeOutputMaterial':
                        nodes.remove(node) 
            print(nodes)
            if len(nodes) == 2:
                for node in nodes:
                    if node.type == 'OUTPUT_MATERIAL':
                        output = node
                    else:
                        color = node
            else:
                acolor = bsdf.inputs[0].default_value
                for node in nodes:
                    if node.type == 'OUTPUT_MATERIAL':
                        output = node
                    color = nodes.new('ShaderNodeRGB')
                    color.outputs[0].default_value = acolor
                
            output.location = (1200,0)
            diff = nodes.new('ShaderNodeBsdfDiffuse')
            diff.location = (0,0)
            srgb = nodes.new('ShaderNodeShaderToRGB')
            srgb.location = (200,0)
            math = nodes.new('ShaderNodeMath')
            math.operation = "POWER"
            math.location = (400,0)
            colorramp = nodes.new('ShaderNodeValToRGB')
            colorramp.location = (600,0)
            if event.ctrl == False and event.alt == False and event.shift == False:
                colorramp.color_ramp.interpolation = 'CONSTANT' 
            if event.ctrl:
                colorramp.color_ramp.interpolation = 'LINEAR'
            colorramp.color_ramp.elements[0].color = (0.1,0.1,0.1,1)
            colorramp.color_ramp.elements[0].position = (0.6)
            colorramp.color_ramp.elements[1].color = (0.4,0.4,0.4,1)
            colorramp.color_ramp.elements[1].position = (0.63)
            colorramp.color_ramp.elements.new(0.780)
            colorramp.color_ramp.elements[2].color = (0.4,0.4,0.4,1)
            colorramp.color_ramp.elements.new(0.80)
            colorramp.color_ramp.elements[3].color = (1,1,1,1)
            math0 = nodes.new('ShaderNodeMixRGB')
            math0.blend_type = "MULTIPLY"
            math0.inputs[0].default_value = 1
            math0.location = (1000,0)
            node_tree = mat.node_tree
            node_tree.links.new(diff.outputs[0],srgb.inputs[0]) 
            node_tree.links.new(srgb.outputs[0],math.inputs[0]) 
            node_tree.links.new(math.outputs[0],colorramp.inputs[0])
            color.location = (600,300) 
            node_tree.links.new(color.outputs[0],math0.inputs[1]) 
            node_tree.links.new(colorramp.outputs[0],math0.inputs[2]) 
            node_tree.links.new(math0.outputs[0],output.inputs[0]) 
        return {"FINISHED"}


class removeunlinknode(bpy.types.Operator):
    """删除所有材质未连接节点"""
    bl_idname = "qk.removeunlinknode"
    bl_label = "删未链接节点"
    def execute(self, context):
        for mat in bpy.data.materials:
            assert (mat is not None and mat.use_nodes), "No material or not node based"
            linked_nodes = set()
            for link in mat.node_tree.links:
                linked_nodes.add(link.from_node)
                linked_nodes.add(link.to_node)           
            unlinked_nodes = set(mat.node_tree.nodes) - linked_nodes
            while unlinked_nodes:
                mat.node_tree.nodes.remove(unlinked_nodes.pop())
        return {"FINISHED"}
class automat(bpy.types.Operator):
    """自动破坏无缝纹理的顺序，直接为平面，ctrl为立体模型"""
    bl_idname = "qk.automat"
    bl_label = "打乱纹理"
    def invoke(self,context,event):
        obj = bpy.context.active_object
        matlist = []
        for mat in obj.material_slots:
            matlist.append(mat)
        for i in range(len(matlist)):
            matname = matlist[i].name
            print(matname)
            mat = bpy.data.materials[matname]
            nodes = mat.node_tree.nodes
            nodeslist = []
            for node in nodes:
                if node.type == "OUTPUT_MATERIAL":
                    output = node
                if node.type == "TEX_COORD":
                    coo = node
                if node.type == "MAPPING":
                    mapping = node
            print(mapping.location)
            l = mapping.location
            node_tree = mat.node_tree
            nodelist = []
            for node in nodes:
                if node.type != "FRAME" and node.type != "OUTPUT_MATERIAL" and node.type != "DISPLACEMENT":
                    nodelist.append(node)
                    node.select = True
                # n = node.copy()
                # n.location = (node.location[0],node.locationi[1]+500)
            override = bpy.context.copy()
            print(bpy.data.screens['Shading'])
            print(bpy.context.screen.areas)
            for a in bpy.data.screens['Shading'].areas:
                print(a.type)
                if a.type == 'NODE_EDITOR':
                    print(a)
                    the_area  = a
            override['area'] = the_area
            bpy.ops.node.clipboard_copy(override)
            bpy.ops.node.clipboard_paste(override)
            for node in nodelist:
                a = node.location
                node.location = (a[0],a[1]-1500)
            
            output.location = (output.location[0]+600,output.location[1]-500)
            texture = nodes.new('ShaderNodeTexCoord')
            texture.location = (l[0]-1000,l[1])
            vor  = nodes.new('ShaderNodeTexVoronoi')
            vor.location = (l[0]-800,l[1])
            node_tree.links.new(texture.outputs[3],vor.inputs[0]) 
            
            texture0= nodes.new('ShaderNodeTexCoord')
            texture0.location = (l[0]+1000,l[1]+500)
            vor0  = nodes.new('ShaderNodeTexVoronoi')
            vor0.location = (l[0]+1200,l[1]+500)
            vor0.feature = 'DISTANCE_TO_EDGE'
            node_tree.links.new(texture0.outputs[3],vor0.inputs[0]) 
            colorramp = nodes.new('ShaderNodeValToRGB')
            colorramp.location = (l[0]+1400,l[1]+500)
            colorramp.color_ramp.interpolation = 'LINEAR'
            colorramp.color_ramp.elements[1].position = (0.0863)
            node_tree.links.new(vor0.outputs[0],colorramp.inputs[0])

            mix = nodes.new('ShaderNodeMixShader')
            mix.location = (l[0]+1700,l[1]+500)
            bsdf = output.inputs[0].links[0].from_node
            print("111111111111111111")
            for node in nodes:
                if node != bsdf and node.type == "BSDF_PRINCIPLED":
                    node_tree.links.new(node.outputs[0],mix.inputs[1])
            node_tree.links.new(colorramp.outputs[0],mix.inputs[0])
            node_tree.links.new(mix.outputs[0],output.inputs[0])
            node_tree.links.new(bsdf.outputs[0],mix.inputs[2])

            texture = nodes.new('ShaderNodeTexCoord')
            texture.location = (l[0]-1000,l[1])
            vor  = nodes.new('ShaderNodeTexVoronoi')
            vor.location = (l[0]-800,l[1])
            node_tree.links.new(texture.outputs[3],vor.inputs[0]) 
            math0 = nodes.new('ShaderNodeMath')
            math0.operation = 'MULTIPLY'
            math0.inputs[1].default_value = 20
            math0.location = (l[0]-600,l[1]+100)
            node_tree.links.new(vor.outputs[1],math0.inputs[0]) 
            node_tree.links.new(math0.outputs[0],mapping.inputs[1]) 
            #平面
            if event.ctrl == False and event.alt == False and event.shift == False:         
                math1 = nodes.new('ShaderNodeMath')
                math1.operation = 'MULTIPLY'
                math1.inputs[1].default_value = 6.2
                math1.location = (l[0]-600,l[1]-100)
                XYZ = nodes.new('ShaderNodeCombineXYZ')
                XYZ.location = (l[0]-400,l[1]-100)
                node_tree.links.new(vor.outputs[1],math1.inputs[0]) 
                node_tree.links.new(math1.outputs[0],XYZ.inputs[2]) 
                node_tree.links.new(XYZ.outputs[0],mapping.inputs[2]) 
            if event.ctrl:
                pass
            val  = nodes.new('ShaderNodeValue')
            val.location = (l[0]-100,l[1]+500)
            val.outputs[0].default_value = 0.5
            node_tree.links.new(val.outputs[0],vor.inputs[2]) 
            node_tree.links.new(val.outputs[0],vor0.inputs[2]) 
            val0  = nodes.new('ShaderNodeValue')
            val0.location = (l[0]-100,l[1]+800)
            val0.outputs[0].default_value = 1
            for node in nodes:
                if node.type == "MAPPING":
                    node_tree.links.new(val0.outputs[0],node.inputs[3])          
        return {"FINISHED"}

class resimtex(bpy.types.Operator):
    """替换同名贴图，多余的保存重启就会删掉"""
    bl_idname = "qk.resimtex"
    bl_label = "替换同名贴图"
    def execute(self, context):
        for img in bpy.data.images:
            if img.name[-3:].isdigit():
                img.name = img.name[:-4]
        for mat in bpy.data.materials:
            if mat.node_tree:
                for n in mat.node_tree.nodes:
                    if n.type == 'TEX_IMAGE':
                        if n.image is None:
                            print(mat.name,'has an image node with no image')
                        elif n.image.name[-3:].isdigit():
                                n.image = bpy.data.images[n.image.name[:-4]]

        for imgs in bpy.data.images:
            if imgs.name[-3:].isdigit():
                print(imgs.name)
                imgs.user_clear()
        return {"FINISHED"}