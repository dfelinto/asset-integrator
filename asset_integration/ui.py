# SPDX-License-Identifier: GPL-2.0-or-later

from .asset_library import (
    add_menu_objects_collections_get,
)

from . import menus

import bpy


def custom_add_menu(elements: list, operator: str):
    def function_template(self, context):
        layout = self.layout
        for key, value in elements:
            layout.operator(operator, text=key)
            # TODO: pass info to operator

            # element=
            # 'Cone': {
            #     'filepath': "Parametric Primitives/Parametric Primitives.blend",
            #     'type': 'OBJECT',
            # },

    return function_template


def populate_menu(menu, content: dict, operator: str):
    elements = []
    for key in content.keys():
        value = content[key]
        is_catalog = not value.get('type')

        if not is_catalog:
            elements.append((key, value))
        else:
            # TODO create menu dynamically
            # submenu = ...
            pass
    menu.append(custom_add_menu(elements, operator))


def populate_object_add_menu():
    content = add_menu_objects_collections_get()

    for key in content.keys():
        value = content[key]
        is_catalog = not value.get('type')

        if key == 'Mesh':
            menu = bpy.types.VIEW3D_MT_mesh_add
            # TODO get the correct operator
            populate_menu(menu, value, "wm.open_mainfile")
            continue

        # TODO if no Menu yet

            # with menus.Menu('Custom Menu') as menu:
            #     with menu.add_submenu('Submenu') as submenu:
            #         submenu.add_operator('mesh.primitive_cube_adad')
            #     menu.add_operator(lambda: 1/0, 'Raise Exception')
            #     menu.register()
            #     menu.unregister()

            # bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unpopulate_object_add_menu():
    pass
    # bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


class DynamicMenu(bpy.types.Menu):
    bl_label = "Dynamic Meny"
    bl_idname = "MT_dynamic_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.open_mainfile")


def register():
    bpy.utils.register_class(DynamicMenu)
    populate_object_add_menu()


def unregister():
    bpy.utils.unregister_class(DynamicMenu)
    unpopulate_object_add_menu()
