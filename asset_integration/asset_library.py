# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

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


def get_all_libraries() -> dict:
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
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Cube': {
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Cylinder': {
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Grid': {
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'Icosphere': {
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
                'UV Sphere': {
                    'filepath': "Parametric Primitives/Parametric Primitives.blend",
                    'type': 'OBJECT',
                },
            },
        }
    }
    library_hair_operators = {
        'Noise':
        {
            'Hair Noise': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            },
            'Hair Noise Proximity': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            },
        },
        'Utilities':
        {
            'Delete Hair': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            },
            'Hair Thickness': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            },
            'Resample': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            }
        },
        'Unassigned':
        {
            'Randomize Length': {
                'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
                'type': 'NODE_TREE',
                'subtype': 'GEOMETRY_NODES',
                'is_modifier': False,
                'is_node': False,
                'is_operator': True,
            }
        }
    }

    library_merged = merge_asset_libraries((
        library_furniture,
        library_human_basemesh,
        library_parametric_primitives,
        library_hair_operators,
    ))
    return library_merged


def passed_rules_filter(element: dict, rules: dict) -> bool:
    """
    Return true if element passes rules filter.
    """
    for key in rules.keys():
        value = element.get(key)
        if not value:
            return False

        rules_values = rules[key]
        if hasattr(rules_values, '__iter__'):
            if value not in rules_values:
                return False
        elif value != rules_values:
            return False
    return True


def filter_dictionary(catalog_dict: dict, rules: dict) -> dict:
    filtered_sub_dictionary = {}

    for key in catalog_dict.keys():
        value = catalog_dict.get(key)
        is_catalog = not value.get('type')

        if not is_catalog:
            if passed_rules_filter(value, rules):
                filtered_sub_dictionary[key] = value
        else:
            sub_dict = filter_dictionary(value, rules)
            if sub_dict:
                filtered_sub_dictionary[key] = sub_dict

    return filtered_sub_dictionary


def add_menu_objects_collections_get() -> dict:
    all_libraries = get_all_libraries()
    return filter_dictionary(all_libraries, {'type': {'OBJECT', 'COLLECTION'}})


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
