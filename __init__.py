# SPDX-License-Identifier: GPL-2.0-or-later

from . import (
    asset_library,
)
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty
from bpy.types import Operator

from bpy.app.handlers import persistent
import bpy
bl_info = {
    "name": "Assets Integration",
    "author": "Blender",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Add",
    "description": "Integrates assets with add menus",
    "warning": "",
    "doc_url": "",
    "category": "Assets",
}


@persistent
def setup_user_preferences(dummy):
    # Most settings can be defined in the userpref.blend for the template
    # however sometimes is more convenient to set the options via Python directly.
    preferences = bpy.context.preferences

    # To prevent an extra userpref.blend file to be
    # create when we change the prefernces we turn
    # this option off.
    #
    # Otherwise during development of the add-on this
    # gets on the way.
    preferences.use_preferences_save = False


@persistent
def setup_asset_library(dummy):
    # After loading a file make sure that the workspace points to the correct asset library.
    asset_library.ensure()
    for workspace in bpy.data.workspaces:
        workspace.asset_library_ref = asset_library.ASSET_LIBRARY_NAME


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    def execute(self, context):
        pass
        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object")


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    bpy.app.handlers.load_post.append(setup_user_preferences)
    bpy.app.handlers.load_post.append(setup_asset_library)

    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.app.handlers.load_post.remove(setup_user_preferences)
    bpy.app.handlers.load_post.remove(setup_asset_library)

    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
