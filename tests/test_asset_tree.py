import unittest

from asset_integration.asset_tree import (
    catalog_read,
    format_uuid,
    get_data_from_library,
    get_uuid_from_asset_data,
)

from asset_integration.asset_library import (
    filter_dictionary,
)


import tempfile
import pathlib


BASE_PATH = pathlib.Path(__file__).parent.absolute()
ASSETS_PATH = BASE_PATH.parent / "sample_asset_library"


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
                'Furniture': {},
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
                'Furniture': {},
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
        blend_filepath = str(ASSETS_PATH / 'Furniture' / 'furniture.blend')
        asset_tree = get_data_from_library(filepath)

        asset_tree_result = {
            'Furniture': {
                'Chair': {
                    'filepath': blend_filepath,
                    'type': 'OBJECT',
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

    def test_basemesh_file(self):
        filepath = str(ASSETS_PATH / 'Human Basemeshes')
        blend_filepath = str(
            ASSETS_PATH / 'Human Basemeshes' / 'human_base_meshes.blend')
        asset_tree = get_data_from_library(filepath)

        asset_tree_result = {
            'Mesh':
            {
                'Human Basemesh':
                {
                    'Eye': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Foot': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Hand': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Jaw': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Stylized Female': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Stylized Head': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                    'Stylized Male': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': '',
                    },
                },
            },
            'Unassigned': {
            }
        }

        self.assertDictEqual(asset_tree_result, asset_tree)

        self.assertDictEqual(
            filter_dictionary(asset_tree_result, {'type': 'OBJECT'}),
            filter_dictionary(asset_tree, {'type': 'OBJECT'}))

    def test_parametric_primitives_file(self):
        filepath = str(ASSETS_PATH / 'Parametric Primitives')
        blend_filepath = str(
            ASSETS_PATH / 'Parametric Primitives' / 'Parametric Primitives.blend')
        asset_tree = get_data_from_library(filepath)

        asset_tree_result = {
            'Mesh':
            {
                'Parametric': {
                    'Cone': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''
                    },
                    'Cube': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''

                    },
                    'Cylinder': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''
                    },
                    'Grid': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''
                    },
                    'Icosphere': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''
                    },
                    'UV Sphere': {
                        'filepath': blend_filepath,
                        'type': 'OBJECT',
                        'description': ''
                    },
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
    def test_uuid_a(self):
        """
        Simple UUID test
        """
        # test simply format_uuid()
        uuid = format_uuid(
            2060775365,
            25763,
            19448,
            181,
            66,
            (20, 250, 180, 31, 232, 245),
        )

        uuid_result = '7ad4efc5-64a3-4bf8-b542-14fab41fe8f5'
        self.assertEqual(uuid, uuid_result)

    def test_uuid_b(self):
        """
        Test UUID with values with low digit (e.g., 9 in the node)
        """
        uuid = format_uuid(
            1410134869,
            7944,
            19313,
            144,
            156,
            (172, 242, 45, 9, 34, 66),
        )

        uuid_result = '540cf355-1f08-4b71-909c-acf22d092242'
        self.assertEqual(uuid, uuid_result)

    def test_uuid_c(self):
        from asset_integration import blendfile

        blend_filepath = str(ASSETS_PATH / 'Furniture' / 'furniture.blend')

        with blendfile.open_blend(blend_filepath) as bf:
            objects = bf.find_blocks_from_code(b'OB')
            for ob in objects:
                asset_data = ob.get_pointer((b'id', b'asset_data'))

                if not asset_data:
                    continue

                ob_name = ob.get((b'id', b'name'))[2:]
                if ob_name != 'Chair':
                    continue

                uuid = get_uuid_from_asset_data(asset_data)
                self.assertEqual(uuid, "7ad4efc5-64a3-4bf8-b542-14fab41fe8f5")
