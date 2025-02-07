# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

"""
Allows running all tests by calling `python3 -m unittest test` from the base directory. This imports all test classes so
that they get run then.
"""

import sys  # To mock entire packages.
import unittest.mock  # To mock away the Blender API.
from .mock.bpy import MockOperator

sys.modules["bpy"] = unittest.mock.MagicMock()
sys.modules["bpy.app"] = unittest.mock.MagicMock()
sys.modules["bpy.app.handlers"] = unittest.mock.MagicMock()
sys.modules["bpy.props"] = unittest.mock.MagicMock()
sys.modules["bpy.types"] = unittest.mock.MagicMock()
sys.modules["bpy.types.Operator"] = MockOperator
sys.modules["bpy_extras"] = unittest.mock.MagicMock()
sys.modules["bpy_extras.object_utils"] = unittest.mock.MagicMock()
sys.modules["bpy_extras.object_utils.AddObjectHelper"] = MockOperator


from .test_asset_tree import *  # nopep8
from .test_asset_library import *  # nopep8
