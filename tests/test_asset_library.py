from asset_integration.asset_library import (
    filter_dictionary,
    merge_asset_libraries,
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


if __name__ == '__main__':
    unittest.main()
