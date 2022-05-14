import bpy
def ShowMessageBox(message = "", title = "提示", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
########################################-Z轴对齐目标、-Y轴对齐
class alignZ(bpy.types.Operator):
    """-Z轴对齐目标(先选被对齐的对象，再选对齐对象）"""
    bl_idname = "qk.ami"
    bl_label = "目标跟随"
    gsz : bpy.props.EnumProperty(
        name="跟随轴",
        description="选择一个",
        items=[
            ("0","X","跟随轴为X"),
            ("1","Y","跟随轴为Y"),
            ("2","Z","跟随轴为Z"),
            ("3","-X","跟随轴为-X"),
            ("4","-Y","跟随轴为-Y"),
            ("5","-Z","跟随轴为-Z"),
        ],
        default='4'
    ) 
    xsz : bpy.props.EnumProperty(
        name="向上轴",
        description="1",
        items=[
            ("0","X","向上轴为X"),
            ("1","Y","向上轴为Y"),
            ("2","Z","向上轴为Z"),
        ],
        default='2'
    ) 
    def execute(self, context):
        gslist =["TRACK_X","TRACK_Y","TRACK_Z","TRACK_NEGATIVE_X","TRACK_NEGATIVE_Y","TRACK_NEGATIVE_Z"]
        uplist =["UP_X","UP_Y","UP_Z"]
        gs = self.gsz
        up = self.xsz
        taget = bpy.context.active_object
        a = bpy.context.selected_objects
        for obj in a:
            if obj != taget:
                a = obj
        print(taget,a)
        bpy.ops.object.constraint_add(type='TRACK_TO')
        c = bpy.data.objects[taget.name].constraints
        try:
            bpy.context.object.constraints[c[-1].name].target = bpy.data.objects[a.name]
            bpy.context.object.constraints[c[-1].name].track_axis = gslist[int(gs)]
            bpy.context.object.constraints[c[-1].name].up_axis = uplist[int(up)]
        except:
            ShowMessageBox(message = "做人要有目标，对象也是", title = "提示", icon = 'INFO')

        
        return {"FINISHED"}
    def draw(self, context):
        layout = self.layout
        layout.prop(self,"gsz")
        layout.prop(self,"xsz")
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)


class targetcon(bpy.types.Operator):
    """为对象在原点建立个空物体为目标，一般用于灯光摄像机"""
    bl_idname = "qk.targetcon"
    bl_label = "添加空目标"
    def execute(self, context):
        ob = bpy.context.active_object
        new_empty = bpy.data.objects.new( "{}目标".format(ob.name), None )
        bpy.context.scene.collection.objects.link( new_empty )
        new_empty.empty_display_type = "SPHERE"
        new_empty.empty_display_size = 0.5
        c = bpy.data.objects[ob.name].constraints
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints[-1].track_axis = 'TRACK_NEGATIVE_Y'
        bpy.context.object.constraints[-1].up_axis = 'UP_Z'
        bpy.context.object.constraints[c[-1].name].target = bpy.data.objects[new_empty.name]
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        bpy.context.view_layer.objects.active = bpy.data.objects[new_empty.name]
        bpy.data.objects[new_empty.name].select_set(True)
        


        return {"FINISHED"}




