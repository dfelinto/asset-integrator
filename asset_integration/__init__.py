# SPDX-License-Identifier: GPL-2.0-or-later

__version__ = '0.1.0'

from . import (
    operator,
    ui,
)

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


def register():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    operator.register()
    ui.register()


def unregister():
    operator.unregister()
    ui.unregister()


if __name__ == "__main__":
    register()
