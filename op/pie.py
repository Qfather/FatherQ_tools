import bpy
from bpy.types import Menu
# from icon_utils import RSN_Preview

###############权重饼图
# import_icon = RSN_Preview(image='import.bip', name='import_icon')

class qk_pie(Menu):
    bl_label = "曲爸爸工具库"
    bl_idname = "QK_MT_tool"

    def draw(self, context):
        global custom_icons
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("qk.automir",icon="MOD_MIRROR")
        pie.operator("qk.view_render",icon="HIDE_OFF")

        other = pie.column()
        other_menu = other.box().column()
        other_menu.scale_y=1.3
        other_menu.operator("qk.hwe",icon="BRUSH_MIX")
        other_menu.operator("qk.wei_point",icon="VPAINT_HLT") 
        other_menu.operator("qk.rand_sel",icon="MOD_ARRAY") 
        other_menu.operator("qk.xcr") 


        other0 = pie.column()
        other_menu0 = other0.box().column()
        other_menu0.scale_y=1.3
        other_menu0.scale_x=1.1
        other_menu0.operator("qk.blfbx",icon="DOCUMENTS") 
        other_menu0.operator("qk.portfbx",icon="EXPORT")
        

        pie.menu('clearmenu', icon='PANEL_CLOSE',  text='清理') 
        pie.menu('othermenu', icon='GHOST_ENABLED',  text='其他') 
        # pie.operator("qk.boneedit",icon="OUTLINER_OB_ARMATURE")
        pie.menu('matmenu', icon='MATERIAL',  text='材质/天空')
        pie.menu('rendermenu', icon='RENDER_STILL',  text='渲染')

###############权重饼图
class wbrush_pie(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "曲爸爸权重工具"
    bl_idname = "QK_MT_wbrush"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("qk.wbrushadd",icon="BRUSH_MIX")
        pie.operator("qk.wbrushsub",icon="BRUSH_BLUR")
        pie.operator("qk.repoint")  
        pie.operator("qk.wset") 
        pie.operator("qk.wbrushblur") 
        pie.operator("qk.wbrushgra") 

class matmenu(Menu):
    bl_label = '材质/天空'    
    def draw(self, context):
        layout = self.layout
        layout.label(text="材质/天空")
        layout.operator("qk.automat", text = "打乱所选无缝纹理",icon='IMAGE_BACKGROUND')
        layout.operator("qk.sp_base_mat", text = "批量赋予不同材质并导出",icon='IMAGE_ALPHA')
        layout.operator("qk.bake_start", text = "开始烘焙",icon='OUTLINER_OB_FORCE_FIELD')
        layout.operator("qk.world_0", text = "添加默认HDR(C随机)",icon='WORLD')
        layout.separator()
        layout.label(text="卡通")
        layout.operator("qk.basect", text = "基础卡通材质",icon='SHADING_SOLID')
        layout.operator("qk.textokt", text = "贴图转卡通",icon='IMAGE_REFERENCE') 
        layout.operator("qk.ctoutline", text = "卡通描边",icon='ANTIALIASED') 
        layout.operator("qk.ctsky", text = "卡通背景HDR",icon='SHADING_WIRE') 
class rendermenu(Menu):
    bl_label = '自定义渲染'    
    def draw(self, context):
        layout = self.layout
        layout.label(text="自定义渲染")
        layout.separator()
        layout.column()
        layout.separator()
        layout.operator("qk.fullrenderselect", text = "渲染所选", icon = "RENDER_STILL")
        layout.operator("qk.renderlayer", text = "分层渲染", icon = "RENDER_RESULT")
        layout.operator("qk.rendersel", text = "渲染所选摄像机", icon = "OUTLINER_OB_CAMERA")
        layout.operator("qk.renderass", text = "渲染所选并分别添加到资产", icon = "ASSET_MANAGER")
        layout.operator("qk.collrender", text = "分别渲染集合内所有对象", icon = "COLLECTION_COLOR_05")
class clearmenu(Menu):
    bl_label = '清理'    
    def draw(self, context):
        layout = self.layout
        layout.label(text="清理")
        layout.separator()
        layout.operator("qk.rmpg",icon="GROUP_VERTEX")
        layout.operator("qk.removemat",icon="CANCEL")
        layout.operator("qk.removeunlinknode",icon='DUPLICATE')
        layout.operator("qk.resimtex",icon='LIBRARY_DATA_BROKEN')
        layout.operator("qk.repoint",icon="LIGHTPROBE_GRID")
        layout.operator("qk.refile",icon="FILEBROWSER")

class othermenu(Menu):
    bl_label = '其他'    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="增强BL")
        col.separator()
        col.operator("qk.bottomcenter",icon="EMPTY_ARROWS")
        col.operator("qk.boneedit",icon="OUTLINER_OB_ARMATURE")
        col.operator("qk.acamera",icon="OUTLINER_OB_CAMERA")
        col.operator("qk.pmove",icon='FILE_VOLUME')
        col.operator("qk.pointcon",icon='CON_OBJECTSOLVER')
        col.operator("qk.plfbx",icon='TEXT')
        col.operator("qk.full",icon='PIVOT_BOUNDBOX')
        col.separator()
        col.operator("qk.tyname",icon='MATSHADERBALL')
        col.operator("qk.num",icon='LINENUMBERS_ON')
        col.separator()
        col.operator("qk.ami",icon='DRIVER')
        col.operator("qk.targetcon",icon='CON_ACTION')
        col.operator("qk.collrandom",icon='COLLECTION_COLOR_06')



        col = row.column()
        col.label(text="骨骼")
        col.separator()
        col.operator("qk.mir",icon="GROUP_BONE")
        col.operator("qk.spring",icon="MOD_SCREW")
        col.operator("qk.btb",icon="KEYINGSET")

        col = row.column()
        col.label(text="形态建")
        col.separator()
        col.operator("qk.sk_start",icon="SHAPEKEY_DATA")
        col.operator("qk.sk_add",icon="ADD")
        col.operator("qk.sk_mir",icon="MOD_MIRROR")


        col = row.column()
        col.label(text="动画")
        col.separator()
        col.operator("qk.offsetkf",icon="KEYINGSET")






