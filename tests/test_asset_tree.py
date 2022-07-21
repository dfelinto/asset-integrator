import unittest

from asset_integration.asset_tree import (
    catalog_read,
    format_uuid,
    get_data_from_library,
    get_uuid_from_object,
)

from asset_integration.asset_library import (
    ASSETS_PATH,
    filter_dictionary,
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


class TestCompleteFile(unittest.TestCase):
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
            'Unassigned': {
            }
        }

        self.assertDictEqual(asset_tree_result, asset_tree)

        self.assertDictEqual(
            filter_dictionary(asset_tree_result, {'type': 'OBJECT'}),
            filter_dictionary(asset_tree, {'type': 'OBJECT'}))

class TestUUID(unittest.TestCase):
    def uuid_a(self):
        # test simply format_uuid()
        pass

    def uuid_b(self):
        from asset_integration import blendfile

        filepath = str(ASSETS_PATH / 'Furniture' / 'furniture.blend' )
        asset_tree = get_data_from_library(filepath)

        with blendfile.open_blend(filepath) as bf:
            objects = bf.find_blocks_from_code(b'OB')
            for ob in objects:
                asset_data = ob.get_pointer((b'id', b'asset_data'))

                if not asset_data:
                    continue

                ob_name = ob.get((b'id', b'name'))[2:]
                if ob_name != 'Chair':
                    continue

                uuid = get_uuid_from_object(ob)
                self.assertEqual(uuid, "7ad4efc5-64a3-4bf8-b542-14fab41fe8f5")
