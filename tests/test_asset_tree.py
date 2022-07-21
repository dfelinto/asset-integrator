import unittest

from asset_integration.asset_tree import (
    catalog_read,
    get_data_from_library,
)

from asset_integration.asset_library import (
    ASSETS_PATH,
)

import os, tempfile

class TestCatalogParser(unittest.TestCase):
    def test_catalog_a(self):
        with tempfile.NamedTemporaryFile(mode='w') as file:
            file.write("""
# This is an Asset Catalog Definition file for Blender.
#
# Empty lines and lines starting with `#` will be ignored.
# The first non-ignored line should be the version indicator.
# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"

VERSION 1

7ad4efc5-64a3-4bf8-b542-14fab41fe8f5:Furniture:Furniture
            """)

            catalog_tree = {}
            catalog_lookup = {}
            catalog_read(file.name, catalog_tree, catalog_lookup)

            catalog_tree_result = {
                'Furniture':{},
            }

            catalog_lookup_result = {
                '7ad4efc5-64a3-4bf8-b542-14fab41fe8f5': catalog_tree_result['Furniture'],
            }

            self.assertDictEqual(catalog_tree_result, catalog_tree_result)
            self.assertDictEqual(catalog_tree_result, catalog_tree_result)


    def test_catalog_b(self):
        with tempfile.NamedTemporaryFile(mode='w') as file:
            file.write("""
# This is an Asset Catalog Definition file for Blender.
#
# Empty lines and lines starting with `#` will be ignored.
# The first non-ignored line should be the version indicator.
# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"

VERSION 1

14937f2a-4b34-42fd-bbfb-f7face8b6954:Mesh:Mesh
e272791e-c4a8-4e8a-b20b-7adc6e97af48:Mesh/Parametric:Mesh-Parametric
7ad4efc5-64a3-4bf8-b542-14fab41fe8f5:Furniture:Furniture
            """)

            catalog_tree = {}
            catalog_lookup = {}
            catalog_read(file.name, catalog_tree, catalog_lookup)

            catalog_tree_result = {
                'Mesh':
                    {
                        'Parametric': {},
                    },
                'Furniture':{},
            }

            catalog_lookup_result = {
                '14937f2a-4b34-42fd-bbfb-f7face8b6954': catalog_tree_result['Mesh'],
                'e272791e-c4a8-4e8a-b20b-7adc6e97af48': catalog_tree_result['Mesh']['Parametric'],
                '7ad4efc5-64a3-4bf8-b542-14fab41fe8f5': catalog_tree_result['Furniture'],
            }

            self.assertDictEqual(catalog_tree_result, catalog_tree_result)
            self.assertDictEqual(catalog_tree_result, catalog_tree_result)


class TestAssetLibrary(unittest.TestCase):
    def test_furniture_file(self):
        filepath = str(ASSETS_PATH / 'Furniture')
        asset_tree = get_data_from_library(filepath)

        asset_tree_result = {
            'Furniture': {
                'Chair': {
                    'filepath': 'Furniture/furniture.blend',
                    'type': 'OBJECT',
                    'description': '',
                },
                'Table': {
                    'filepath': 'Furniture/furniture.blend',
                    'type': 'COLLECTION',
                    'description': '',
                },
            },
        }
        self.assertDictEqual(asset_tree_result, asset_tree)
