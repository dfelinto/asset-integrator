from asset_integration.asset_library import (
    filter_dictionary,
    merge_asset_libraries,
    is_asset,
    is_catalog,
)
from asset_integration import (
    __version__,
)
import unittest

from .mock.bpy import MockOperator


import bpy.types
bpy.types.Operator = MockOperator


def test_version():
    assert __version__ == '0.1.0'


class TestCatalogParser(unittest.TestCase):

    def test_catalog(self):
        library_a = {
            'Mesh':
            {
                'My Objects':
                {
                    'A': {},
                    'B': {},
                },
            },
        }
        library_b = {
            'Mesh':
            {
                'My Objects':
                {
                    'C': {},
                },
                'Other Objects':
                {
                    'D': {},
                }
            },
        }
        library_result = {
            'Mesh':
            {
                'My Objects':
                {
                    'A': {},
                    'B': {},
                    'C': {},
                },
                'Other Objects':
                {
                    'D': {},
                }
            },
        }

        self.assertDictEqual(
            library_result, merge_asset_libraries((library_a, library_b)),
        )

    def test_simpler_catalog(self):
        library_a = {
            'Objects':
            {
                'Cube': {
                    'type': 'OBJECT',
                },
                'Material': {
                    'type': 'MATERIAL',
                },
                'Sub Catalog':
                {
                    'Cone': {
                        'type': 'OBJECT',
                    },
                }
            }
        }

        library_b = {
            'Objects':
            {
                'Grid': {
                    'type': 'OBJECT',
                },
                'Sub Catalog':
                {
                    'Pyramid': {
                        'type': 'OBJECT',
                    },
                }
            }
        }

        library_result = {
            'Objects':
            {
                'Cube': {
                    'type': 'OBJECT',
                },
                'Grid': {
                    'type': 'OBJECT',
                },
                'Material': {
                    'type': 'MATERIAL',
                },
                'Sub Catalog':
                {
                    'Cone': {
                        'type': 'OBJECT',
                    },
                    'Pyramid': {
                        'type': 'OBJECT',
                    },
                }
            }
        }

        self.assertDictEqual(
            library_result, merge_asset_libraries((library_a, library_b)),
        )


class TestCatalogFilter(unittest.TestCase):
    library_all = {
        'My Catalog':
        {
            'My Objects and Collections':
            {
                'A': {'type': 'OBJECT'},
                'B': {'type': 'COLLECTION'},
            },
            'My Materials':
            {
                'C': {'type': 'MATERIAL'}
            },
            'My Nodes':
            {
                'D': {
                    'type': 'NODE_TREE',
                    'subtype': 'GEOMETRY_NODES',
                    'is_modifier': False,
                    'is_node': False,
                    'is_operator': True,
                },
                'E': {
                    'type': 'NODE_TREE',
                    'subtype': 'GEOMETRY_NODES',
                    'is_modifier': False,
                    'is_node': True,
                    'is_operator': True,
                },
                'F': {
                    'type': 'NODE_TREE',
                    'subtype': 'GEOMETRY_NODES',
                    'is_modifier': False,
                    'is_node': True,
                    'is_operator': True,
                },
                'G': {
                    'type': 'NODE_TREE',
                    'subtype': 'SHADING',
                    'is_modifier': False,
                    'is_node': True,
                    'is_operator': True,
                },
            },
        },
    }

    def test_filter_object_and_collections(self):
        library_result = {
            'My Catalog':
            {
                'My Objects and Collections':
                {
                    'A': {'type': 'OBJECT'},
                    'B': {'type': 'COLLECTION'},
                },
            }
        }

        self.assertDictEqual(
            library_result, filter_dictionary(
                self.library_all, {'type': {'OBJECT', 'COLLECTION'}})
        )

    def test_filter_object(self):
        library_result = {
            'My Catalog':
            {
                'My Objects and Collections':
                {
                    'A': {'type': 'OBJECT'},
                },
            }
        }

        self.assertDictEqual(
            library_result, filter_dictionary(
                self.library_all, {'type': 'OBJECT'})
        )

    def test_filter_nodes(self):
        library_result = {
            'My Catalog':
            {
                'My Nodes':
                {
                    'E': {
                        'type': 'NODE_TREE',
                        'subtype': 'GEOMETRY_NODES',
                        'is_modifier': False,
                        'is_node': True,
                        'is_operator': True,
                    },
                    'F': {
                        'type': 'NODE_TREE',
                        'subtype': 'GEOMETRY_NODES',
                        'is_modifier': False,
                        'is_node': True,
                        'is_operator': True,
                    },
                },
            }
        }

        self.assertDictEqual(
            library_result, filter_dictionary(
                self.library_all, {
                    'type': 'NODE_TREE',
                    'subtype': 'GEOMETRY_NODES',
                    'is_node': True,
                })
        )

    def test_simpler_catalog(self):
        library = {
            'Objects':
            {
                'Cube': {
                    'type': 'OBJECT',
                },
                'Material': {
                    'type': 'MATERIAL',
                },
                'Sub Catalog':
                {
                    'Cone': {
                        'type': 'OBJECT',
                    },
                }
            }
        }

        library_result = {
            'Objects':
            {
                'Cube': {
                    'type': 'OBJECT',
                },
                'Sub Catalog':
                {
                    'Cone': {
                        'type': 'OBJECT',
                    },
                }
            }
        }

        self.assertDictEqual(
            library_result, filter_dictionary(
                library, {
                    'type': 'OBJECT',
                })
        )


class TestCatalog(unittest.TestCase):
    library = {
        'My Catalog':
        {
            'Sub Catalog':
            {
                'A': {'type': 'OBJECT'},
                'B': {'type': 'COLLECTION'},
            },
        }
    }

    def test_is_catalog_a(self):
        self.assertTrue(is_catalog(self.library))
        self.assertFalse(is_asset(self.library))

    def test_is_catalog_b(self):
        sub_library = self.library.get('My Catalog')
        self.assertTrue(is_catalog(sub_library))
        self.assertFalse(is_asset(sub_library))

    def test_is_asset(self):
        sub_library = self.library.get('My Catalog').get("Sub Catalog")
        asset_a = sub_library.get("A")
        asset_b = sub_library.get("B")

        self.assertTrue(is_asset(asset_a))
        self.assertFalse(is_catalog(asset_a))

        self.assertTrue(is_asset(asset_b))
        self.assertFalse(is_catalog(asset_b))


if __name__ == '__main__':
    unittest.main()
