# SPDX-License-Identifier: GPL-2.0-or-later

__version__ = '0.1.0'


from . import (
    asset_library,
    operator,
    ui,
)

from bpy_extras.object_utils import AddObjectHelper
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


def register():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    bpy.app.handlers.load_post.append(setup_user_preferences)
    bpy.app.handlers.load_post.append(setup_asset_library)

    operator.register()
    ui.register()


def unregister():
    bpy.app.handlers.load_post.remove(setup_user_preferences)
    bpy.app.handlers.load_post.remove(setup_asset_library)

    operator.unregister()
    ui.unregister()


if __name__ == "__main__":
    register()
