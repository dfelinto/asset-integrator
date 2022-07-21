# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

from .asset_tree import (
    generate_asset_tree,
)

import logging
logger = logging.getLogger(__name__)


def is_asset(content: dict) -> bool:
    """
    Return whether the dictionary is an asset.
    """
    return "type" in content


def is_catalog(content: dict) -> bool:
    """
    Return whether the dictionary is a catalog.
    """
    return not is_asset(content)


all_libraries = {}


def get_all_libraries() -> dict:
    """
    Returns a nested dictionary with all the assets.
    """
    if all_libraries:
        return all_libraries

    all_libraries.update(generate_asset_tree())
    return all_libraries


def passed_rules_filter(element: dict, rules: dict) -> bool:
    """
    Return true if element passes rules filter.

    If the rules value has an iterator, it assumes that it should be tested
    against each individual value.
    """
    for key in rules.keys():
        value = element.get(key)
        if value is None:
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


def add_menu_geometry_nodes_get() -> dict:
    all_libraries = get_all_libraries()
    return filter_dictionary(all_libraries,
                             {
                                 'type': 'NODE_TREE',
                                 'subtype': 'GEOMETRY_NODES',
                                 'is_node': True,
                             })


def operator_tools_curves_geometry_nodes_get() -> dict:
    all_libraries = get_all_libraries()
    return filter_dictionary(all_libraries,
                             {
                                 'type': 'NODE_TREE',
                                 'subtype': 'GEOMETRY_NODES',
                                 'is_operator': True,
                             })


def merge_dict_recursive(dict_final: dict, dict_iter: dict):
    """
    Recursively combine dictionaries based on their keys
    """
    for key in dict_iter.keys():
        if dict_final.get(key):
            merge_dict_recursive(dict_final[key], dict_iter[key])
        else:
            dict_final[key] = dict_iter[key].copy()


def merge_asset_libraries(libraries: list) -> dict:
    """
    Merge multiple libraries

    The catalogs are merged together.
    """
    library_merged = {}
    for library_iter in libraries:
        merge_dict_recursive(library_merged, library_iter)
    return library_merged
