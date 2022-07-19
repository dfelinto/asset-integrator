# SPDX-License-Identifier: GPL-2.0-or-later

import bpy


class OBJECT_OT_add_asset_object(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.add_asset_object"
    bl_label = "Add Asset Object"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")

    def execute(self, context):
        # TODO actual implementation (call other script)
        print(self.filepath)
        return {'FINISHED'}


class NODES_OT_add_asset_node(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "nodes.add_asset_node"
    bl_label = "Add Asset Node"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")

    def execute(self, context):
        # TODO actual implementation (call other script)
        print(self.filepath)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_add_asset_object)
    bpy.utils.register_class(NODES_OT_add_asset_node)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_asset_object)
    bpy.utils.unregister_class(NODES_OT_add_asset_node)
