import unittest

from .mock.bpy import MockOperator


import bpy.types
bpy.types.Operator = MockOperator

from asset_integration import (
    __version__,
)

from asset_integration.asset_library import (
    merge_asset_libraries,
)


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


if __name__ == '__main__':
    unittest.main()
