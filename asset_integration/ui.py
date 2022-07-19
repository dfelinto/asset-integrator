# SPDX-License-Identifier: GPL-2.0-or-later

from .asset_library import (
    add_menu_objects_collections_get,
    get_asset_filepath,
    is_catalog,
)

from .operator import (
    OBJECT_OT_add_asset_object,
)

import bpy


def custom_add_menu(elements: list, operator: str):
    def function_template(self, context):
        layout = self.layout
        layout.separator()
        for key, value in elements:
            operator_props = layout.operator(operator, text=key)
            operator_props.id_name = key
            operator_props.filepath = str(
                get_asset_filepath(value['filepath']))

    return function_template


def populate_menu(menu, content: dict, operator: str):
    elements = []
    for key in sorted(content.keys()):
        value = content[key]
        if not is_catalog(value):
            elements.append((key, value))
        else:
            # TODO create menu dynamically
            # submenu = ...
            #
            pass
    menu.append(custom_add_menu(elements, operator))


def populate_object_add_menu():
    # TODO other hard-coded categories
    menus_lookup = {
        'Mesh': bpy.types.VIEW3D_MT_mesh_add,
        'Curve': bpy.types.VIEW3D_MT_curve_add,
    }

    content = add_menu_objects_collections_get()
    elements = {}

    for key in content.keys():
        value = content[key]

        menu = menus_lookup.get(key)

        if is_catalog(value) and menu:
            populate_menu(menu, value, OBJECT_OT_add_asset_object.bl_idname)
        else:
            elements[key] = value

    populate_menu(bpy.types.VIEW3D_MT_add, elements,
                  OBJECT_OT_add_asset_object.bl_idname)


def unpopulate_object_add_menu():
    # TODO unregister everything
    pass


class ASSET_MT_DynamicMenu(bpy.types.Menu):
    bl_idname = "ASSET_MT_DynamicMenu"
    bl_label = "Dynamic Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.open_mainfile")


def register():
    bpy.utils.register_class(ASSET_MT_DynamicMenu)
    populate_object_add_menu()


def unregister():
    bpy.utils.unregister_class(ASSET_MT_DynamicMenu)
    unpopulate_object_add_menu()
