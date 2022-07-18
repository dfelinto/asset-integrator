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


def add_menu_objects_collections_get() -> dict:
    """
    Returns a nested dictionary with all the assets
    """
    library_furniture = {
        'Furniture': {
            'Chair': {
                'filepath': "Furniture/furniture.blend",
                'type': 'OBJECT',
            },
            'Table': {
                'filepath': "Furniture/furniture.blend",
                'type': 'COLLECTION',
            }
        },
    }
    library_human_basemesh = {
        'Mesh':
        {
            'Human Basemesh':
            {
                'Eye': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Foot': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Hand': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Jaw': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Stylized Female': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Stylized Head': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
                'Stylized Male': {
                    'filepath': "Human Basemeshes/human_base_meshes.blend",
                    'type': 'OBJECT',
                },
            },
        },
    }
    library_parametric_primitives = {
        'Mesh':
        {
            'Parametric': {
                'Cone': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Cube': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Cylinder': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Grid': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Icosphere': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'UV Sphere': {
                    'filepath': "/home/dfelinto/Documents/projects/2022/node-tools/assets-integration-prototype/repositories/Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
            },
        }
    }

    library_merged = merge_asset_libraries((
        library_furniture,
        library_human_basemesh,
        library_parametric_primitives,
    ))
    return library_merged


def merge_dict_recursive(dict_final: dict, dict_iter: dict):
    """
    Recursively combine dictionaries based on their keys
    """
    for key in dict_iter.keys():
        if dict_final.get(key):
            merge_dict_recursive(dict_final[key], dict_iter[key])
        else:
            dict_final[key] = dict_iter[key]


def merge_asset_libraries(libraries: list) -> dict:
    """
    Merge multiple libraries

    The catalogs are merged together.
    """
    library_merged = {}
    for library_iter in libraries:
        merge_dict_recursive(library_merged, library_iter)
    return library_merged
