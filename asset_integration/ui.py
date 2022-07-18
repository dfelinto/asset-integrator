# SPDX-License-Identifier: GPL-2.0-or-later

from .asset_library import (
    add_menu_objects_collections_get,
)


def add_object_button(self, context):
    pass
    # self.layout.operator(
    #    OBJECT_OT_add_object.bl_idname,
    #    text="Add Object")


def populate_object_add_menu():
    content = add_menu_objects_collections_get()
    print(content)

    pass
    # bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unpopulate_object_add_menu():
    pass
    # bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


def register():
    populate_object_add_menu()


def unregister():
    unpopulate_object_add_menu()
