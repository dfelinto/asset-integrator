# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

import bpy
import pathlib

import logging

logger = logging.getLogger(__name__)

ASSET_LIBRARY_NAME = "Blender Bundle"
BASE_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = BASE_PATH / "repositories"


def ensure() -> None:
    """
    Ensure that the asset library is configured.
    """
    prefs = bpy.context.preferences
    asset_lib = prefs.filepaths.asset_libraries.get(ASSET_LIBRARY_NAME)
    if not asset_lib:
        bpy.ops.preferences.asset_library_add()
        asset_lib = prefs.filepaths.asset_libraries[-1]
        asset_lib.name = ASSET_LIBRARY_NAME

    asset_lib.path = str(ASSETS_PATH)
