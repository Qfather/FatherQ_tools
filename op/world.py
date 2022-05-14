import bpy
import os
import random
#########################################批量索引后缀
class world_0(bpy.types.Operator):
    """添加森林HDR，Ctrl点击随机添加blender内置HDR"""
    bl_idname = "qk.world_0"
    bl_label = "HDR"
    def invoke(self,context,event):
        world = bpy.data.worlds[0]
        world.use_nodes = True
        nodes = world.node_tree.nodes
        path = bpy.utils.script_paths()[1][:-7]+"datafiles\\studiolights\\world\\"
        files = os.listdir(path)
        files.remove("license.txt")
        nodes.clear()
        node_background = nodes.new(type='ShaderNodeBackground')
        node_environment = nodes.new('ShaderNodeTexEnvironment')
        if event.ctrl == False and event.alt == False and event.shift == False:
            node_environment.image = bpy.data.images.load(path+files[2])   
        if event.ctrl:
            a = random.randint(0,6)
            node_environment.image = bpy.data.images.load(path+files[a]) 
        node_environment.location = -300,0
        node_output = nodes.new(type='ShaderNodeOutputWorld')   
        node_output.location = 200,0
        links = world.node_tree.links
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"])
        return {"FINISHED"}
class ctsky(bpy.types.Operator):
    """替换第一个材质为卡通天空"""
    bl_idname = "qk.ctsky"
    bl_label = "卡通天空"
    a:bpy.props.FloatVectorProperty(  
                                    name="颜色",
                                    subtype='COLOR',
                                    default=(0.053, 0.34, 1.0),
                                    min=0.0, max=1.0,
                                    description="color picker"
                                    )
    
    def execute(self, context):
        col = self.a 
        world = bpy.data.worlds[0]
        world.use_nodes = True
        nodes = world.node_tree.nodes
        nodes.clear()
        node_tree = world.node_tree
        geo = nodes.new('ShaderNodeNewGeometry')
        geo.location = (0,0)

        mapping = nodes.new('ShaderNodeMapping')
        mapping.vector_type = 'POINT'
        mapping.inputs[1].default_value[0] = 0.25
        mapping.inputs[2].default_value[1] = 1.5708
        mapping.location = (200,0)

        node_tree.links.new(geo.outputs[0],mapping.inputs[0]) 

        texgra = nodes.new('ShaderNodeTexGradient')
        texgra.gradient_type = 'EASING'
        texgra.location = (400,0)
        node_tree.links.new(mapping.outputs[0],texgra.inputs[0]) 

        colorramp = nodes.new('ShaderNodeValToRGB')
        colorramp.location = (600,0)
        colorramp.color_ramp.elements[0].color = (1,1,1,1)
        colorramp.color_ramp.elements[0].position = (0.17)
        colorramp.color_ramp.elements[1].color = (0.2,0.2,0.2,1)
        colorramp.color_ramp.elements[1].position = (0.75)
        rgb = nodes.new('ShaderNodeRGB')
        rgb.location = (600,-300)
        rgb.outputs[0].default_value = (col[0],col[1],col[2],1)
        node_tree.links.new(texgra.outputs[0],colorramp.inputs[0])
        math0 = nodes.new('ShaderNodeMixRGB')
        math0.blend_type = "MIX"
        math0.inputs[1].default_value = (0, 0, 0, 1)
        math0.location = (1000,0)

        math1 = nodes.new('ShaderNodeMixRGB')
        math1.blend_type = "MULTIPLY"
        math1.inputs[0].default_value = 1
        math1.location = (900,-150)
        light = nodes.new('ShaderNodeLightPath')
        light.location = (800,300)

        node_tree.links.new(colorramp.outputs[0],math1.inputs[1])
        node_tree.links.new(rgb.outputs[0],math1.inputs[2])
        node_tree.links.new(math1.outputs[0],math0.inputs[2])
        node_tree.links.new(light.outputs[0],math0.inputs[0])

        node_output = nodes.new(type='ShaderNodeOutputWorld') 
        node_output.location = 1200,0
        node_tree.links.new(math0.outputs[0],node_output.inputs[0])
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"a")
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

        
    