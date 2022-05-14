bl_info = {
    "name": "曲爸爸的工具库!!!",
    "author": "曲爸爸",
    "version": (2, 0),
    "blender": (3, 0, 0),
    "location": "N面板，资产摄像机，隐藏的轴心到中心下方",
    "description": "各种工具",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}
import bpy
import os
import bpy.props
from .op.name import tyname,num,refile
from .op.custom_render import collrender,renderlayer,fullrenderselect,full,rendersel,renderass
from .op.sort import collrandom,rand_sel
from .op.blender_pro import acamera,bottomcenter,EportFBX,view_render,pmove,pointcon,boneedit,automir,blfbx
from .op.target import alignZ,targetcon
from .op.weight import wset,wei_point,rmpg,hwe,wbrush_add,wbrush_sub,repoint,wbrush_blur,wbrush_gra
from .op.bone import btb,mir,spring
from .op.work import XCR
from .op.anim import offsetkf
from .op.shape_keys import sk_start,sk_add,sk_mir
from .op.mat import removemat,sp_base_mat,ctoutline,basect,textokt,removeunlinknode,automat,resimtex
from .op.bake import bake_start
from .op.world import world_0,ctsky
from .op.pie import qk_pie,wbrush_pie,matmenu,rendermenu,clearmenu,othermenu
# from icon_utils import RSN_Preview





# class TDR_Panel_Base(bpy.types.Panel):
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "曲爸爸"
    
#     #总UI类

#     def draw(self, context):
#         layout = self.layout
    #Panel好像一定要有这个attribute

# class blender_pro(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_blenderpro"
#     bl_label = "增强BL"
#     def draw(self, context):
#         global custom_icons
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.acamera",icon_value=custom_icons["资产像机"].icon_id)
#         row = layout.row(align=True)
#         row.operator("qk.pmove",icon_value=custom_icons["队列"].icon_id)
#         row.operator("qk.pointcon",icon_value=custom_icons["点控制器"].icon_id)
#         row = layout.row(align=True)
#         row.operator("qk.plfbx",icon_value=custom_icons["导出FBX"].icon_id)
#         row.operator("qk.full",icon_value=custom_icons["充满摄像机"].icon_id)
# class matname(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_matname"
#     bl_label = "批量命名"
#     bl_parent_id = "QK_PT_blenderpro"
#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.tyname",icon_value=custom_icons["名称统一"].icon_id)
#         row.operator("qk.num",icon_value=custom_icons["NUM"].icon_id)
#         row.operator("qk.refile")
     
          






# class sort(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_sort"
#     bl_label = "排序"
#     bl_parent_id = "QK_PT_blenderpro"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
        
#         row.operator("qk.rand_sel",icon_value=custom_icons["子集随机"].icon_id)
#         row.operator("qk.collrandom",icon_value=custom_icons["合集随机"].icon_id)
# class target(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_target"
#     bl_label = "目标约束"
#     bl_parent_id = "QK_PT_blenderpro"
#     def draw(self, context):
#         global custom_icons
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.ami",icon_value=custom_icons["目标跟随"].icon_id)
#         row.operator("qk.targetcon",icon_value=custom_icons["添加空目标"].icon_id)

# class bd(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_bd"
#     bl_label = "绑定修型"

#     def draw(self, context):
#         layout = self.layout

# class weight(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_weight"
#     bl_label = "权重工具"
#     bl_parent_id = "QK_PT_bd"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.wei_point",icon_value=custom_icons["对齐权重"].icon_id)
#         row.operator("qk.hwe",icon_value=custom_icons["传递权重"].icon_id)
# class bone(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_bone"
#     bl_label = "骨骼"
#     bl_parent_id = "QK_PT_bd"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.btb",icon_value=custom_icons["对齐骨骼"].icon_id)
#         row.operator("qk.mir",icon_value=custom_icons["镜像骨骼"].icon_id)
#         row.operator("qk.spring")
# class shape_keys(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_shapekeys"
#     bl_label = "形态建"
#     bl_parent_id = "QK_PT_bd"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.sk_start",icon_value=custom_icons["开始形态"].icon_id)
#         row.operator("qk.sk_add",icon_value=custom_icons["增加形态"].icon_id)
#         row.operator("qk.sk_mir",icon_value=custom_icons["镜像形态"].icon_id)
# class anima(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_anima"
#     bl_label = "动画"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.offsetkf",icon_value=custom_icons["偏移关键帧"].icon_id)
# class work(TDR_Panel_Base):
    
#     bl_idname = "QK_PT_work"
#     bl_label = "工作"

#     def draw(self, context):
#         layout = self.layout
#         row = layout.row()
#         row.operator("qk.xcr",icon_value=custom_icons["清理香肠人"].icon_id)


#######快捷键


classes = [

    #RSN_Preview,
    #一级目录ui
    # blender_pro,
    # bd,
    # anima,
    # work,
    # #二级目录
    # matname,
    # sort,
    # target,
    # weight,
    # bone,
    # shape_keys,
    
    
    #快捷键

    #name
    tyname,refile,


    #自定义渲染
    collrender,
    renderlayer,
    fullrenderselect,
    full,rendersel,renderass,
    #排序
    collrandom,
    rand_sel,
    #增强 bl
    acamera,
    bottomcenter,
    EportFBX,
    view_render,
    pmove,
    pointcon,boneedit,num,automir,blfbx,
    #目标
    alignZ,targetcon,
    #权重
    wset,wei_point,rmpg,hwe,wbrush_add,wbrush_pie,wbrush_sub,repoint,wbrush_blur,wbrush_gra,
    #骨骼
    btb,mir,spring,
    #动画
    offsetkf,
    #工作
    XCR,
    #形态建
    sk_start,sk_add,sk_mir,
    #材质
    removemat,
    sp_base_mat,ctoutline,basect,textokt,removeunlinknode,automat,resimtex,
    #烘焙
    bake_start,
    #hdr
    world_0,ctsky,
    #pie
    qk_pie,matmenu,rendermenu,clearmenu,othermenu,




]
#批量注册

custom_icons = None#图标
#快捷键
addon_keymaps = []
def register():
    #自定义图标
    # global custom_icons
    # custom_icons = bpy.utils.previews.new()
    # addon_path =  os.path.dirname(__file__)
    # icons_dir = os.path.join(addon_path, "icons")

    # for entry in os.scandir(icons_dir):
    #     if entry.name.endswith(".png"):
    #         name = os.path.splitext(entry.name)[0]
    #         custom_icons.load(name.upper(), os.path.join(icons_dir, entry.path), 'IMAGE')
    for clas in classes:
        bpy.utils.register_class(clas)


    ################设置快捷键
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Weight Paint', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', ctrl=False, shift=True)
    kmi.properties.name = "QK_MT_wbrush"
    addon_keymaps.append((km,kmi))

    tool = wm.keyconfigs.addon.keymaps.new("3D View", space_type='VIEW_3D')
    tooli = tool.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', ctrl=False, shift=True)
    tooli.properties.name = "QK_MT_tool"
    addon_keymaps.append((tool,tooli))

    
    print('register')
    


def unregister():
    #properties.unregister()
    # global custom_icons
    # bpy.utils.previews.remove(custom_icons)
    for clas in classes:
        bpy.utils.unregister_class(clas)
    # handle the keymap
    wm = bpy.context.window_manager
    for a, b in addon_keymaps:
        a.keymap_items.remove(b)
    # clear the list
    del addon_keymaps[:]
    
#注册与注销


if __name__ == "__main__":
    __file__ = bpy.data.filepath
    register()
    
    
