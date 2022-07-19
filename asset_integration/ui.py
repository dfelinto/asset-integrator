# SPDX-License-Identifier: GPL-2.0-or-later

from unittest.mock import NonCallableMagicMock
from .asset_library import (
    add_menu_geometry_nodes_get,
    add_menu_objects_collections_get,
    get_asset_filepath,
    is_catalog,
    is_asset,
)

from .operator import (
    OBJECT_OT_add_asset_object,
    NODES_OT_add_asset_node,
)

import bpy


class MenuItem:
    _is_catalog = False
    _name = ""
    _asset = {}

    def __init__(self, name, asset):
        self._name = name
        self._is_catalog = is_catalog(asset)
        self._asset = asset


def set_operator_properties(props, name: str, asset: dict):
    props.id_name = name
    props.filepath = str(get_asset_filepath(asset['filepath']))


def custom_add_menu(elements: list, operator: str):
    def function_template(self, context):
        layout = self.layout
        layout.separator()
        for element in elements:
            if element._is_catalog:
                row = layout.row()
                row.context_pointer_set(CONTEXT_ID, row)
                ASSET_MT_DynamicMenu._parents[row] = (
                    None, MenuPayload(element._asset, operator))
                row.menu(ASSET_MT_DynamicMenu.bl_idname, text=element._name)
            else:
                operator_props = layout.operator(operator, text=element._name)
                set_operator_properties(
                    operator_props, element._name, element._asset)

    return function_template


def populate_menu_doit(menu, content: dict, operator: str):
    elements = []
    for key in sorted(content.keys()):
        value = content[key]
        elements.append(MenuItem(key, value))
    menu.append(custom_add_menu(elements, operator))


def populate_menu(menus: list, main_menu: bpy.types.Menu, content: dict, operator_name: str):
    """
    Populates a menu dynamically.
    """
    menus_lookup = {menu.bl_label: menu for menu in menus}
    elements = {}

    for key in content.keys():
        value = content[key]

        menu = menus_lookup.get(key)

        if is_catalog(value) and menu:
            populate_menu_doit(menu, value, operator_name)
        else:
            elements[key] = value

    populate_menu_doit(main_menu, elements, operator_name)


def populate_object_add_menu():
    """
    Populate the viewport add menu.
    """
    # TODO other hard-coded categories such as grease pencil and empty
    menus = (
        bpy.types.VIEW3D_MT_mesh_add,
        bpy.types.VIEW3D_MT_curve_add,
        bpy.types.VIEW3D_MT_surface_add,
        bpy.types.VIEW3D_MT_metaball_add,
        bpy.types.VIEW3D_MT_volume_add,
        bpy.types.VIEW3D_MT_armature_add,
        bpy.types.VIEW3D_MT_image_add,
        bpy.types.VIEW3D_MT_light_add,
        bpy.types.VIEW3D_MT_lightprobe_add,
        bpy.types.VIEW3D_MT_camera_add,
    )
    content = add_menu_objects_collections_get()
    populate_menu(menus, bpy.types.VIEW3D_MT_add,
                  content, OBJECT_OT_add_asset_object.bl_idname)


def populate_geometry_nodes_add_menu():
    """
    Populate the Geometry Nodes add nodes menus.
    """
    menus = (
        bpy.types.NODE_MT_category_GEO_ATTRIBUTE,
        bpy.types.NODE_MT_category_GEO_COLOR,
        bpy.types.NODE_MT_category_GEO_CURVE,
        bpy.types.NODE_MT_category_GEO_PRIMITIVES_CURVE,
        bpy.types.NODE_MT_category_GEO_GEOMETRY,
        bpy.types.NODE_MT_category_GEO_INPUT,
        bpy.types.NODE_MT_category_GEO_INSTANCE,
        bpy.types.NODE_MT_category_GEO_MESH,
        bpy.types.NODE_MT_category_GEO_PRIMITIVES_MESH,
        bpy.types.NODE_MT_category_GEO_OUTPUT,
        bpy.types.NODE_MT_category_GEO_POINT,
        bpy.types.NODE_MT_category_GEO_TEXT,
        bpy.types.NODE_MT_category_GEO_TEXTURE,
        bpy.types.NODE_MT_category_GEO_UTILITIES,
        bpy.types.NODE_MT_category_GEO_UV,
        bpy.types.NODE_MT_category_GEO_VECTOR,
        bpy.types.NODE_MT_category_GEO_VOLUME,
        bpy.types.NODE_MT_category_GEO_GROUP,
        bpy.types.NODE_MT_category_GEO_LAYOUT,
    )
    menus_lookup = {menu.bl_label: menu for menu in menus}

    content = add_menu_geometry_nodes_get()
    populate_menu(menus, bpy.types.NODE_MT_add,
                  content, NODES_OT_add_asset_node.bl_idname)


CONTEXT_ID = "dynamic_menu_id"


class MenuPayload:
    _asset = {}
    _operator = ""

    def __init__(self, asset: dict, operator: str):
        self._asset = asset
        self._operator = operator


class ASSET_MT_DynamicMenu(bpy.types.Menu):
    bl_label = "Dynamic Menu"
    bl_idname = "ASSET_MT_DynamicMenu"

    _parents = {}

    @staticmethod
    def _calc_path(layout):
        """
        Accumulate a list of payloads and return them in-order.
        """
        result = []
        while layout:
            layout, payload = ASSET_MT_DynamicMenu._parents.get(
                layout, (None, None))
            result.append(payload)
        result.reverse()
        return result

    def draw(self, context):
        layout = self.layout
        parent_id = getattr(context, CONTEXT_ID, None)

        if parent_id is None:
            ASSET_MT_DynamicMenu._parents.clear()
            return

        payload = ASSET_MT_DynamicMenu._calc_path(parent_id)[0]
        asset_tree = payload._asset
        operator = payload._operator

        for key in asset_tree.keys():
            value = asset_tree.get(key)

            if is_asset(value):
                operator_props = layout.operator(operator, text=key)
                set_operator_properties(operator_props, key, value)
            else:
                row = layout.row()
                row.context_pointer_set(CONTEXT_ID, row)
                ASSET_MT_DynamicMenu._parents[row] = (
                    parent_id, MenuPayload(value, operator))
                row.menu(ASSET_MT_DynamicMenu.bl_idname, text=key)


def register():
    bpy.utils.register_class(ASSET_MT_DynamicMenu)
    populate_object_add_menu()
    populate_geometry_nodes_add_menu()


def unregister():
    bpy.utils.unregister_class(ASSET_MT_DynamicMenu)
