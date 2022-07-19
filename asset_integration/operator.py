# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import os


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
    """Add node group node"""
    bl_idname = "nodes.add_asset_node"
    bl_label = "Add Asset Node"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")

    def execute(self, context):
        if self.id_name not in bpy.data.node_groups:
            file_path = self.filepath
            inner_path = 'NodeTree'
            asset_name = self.id_name

            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, asset_name),
                directory=os.path.join(file_path, inner_path),
                filename=asset_name
                )
            bpy.data.node_groups.get(self.id_name).asset_clear()

        bpy.ops.node.add_node(
            type="GeometryNodeGroup",
            use_transform=True,
            settings=[
                {
                    "name":"node_tree",
                    "value":"bpy.data.node_groups['{}']".format(self.id_name),
                }])

        return {'FINISHED'}


class NODES_OT_asset_operator(bpy.types.Operator):
    """Run node group tool"""
    bl_idname = "nodes.add_asset_operator"
    bl_label = "Add Asset Operator"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")

    def execute(self, context):
        # TODO actual implementation (call other script)
        print(self.filepath)
        return {'FINISHED'}


classes = (
    OBJECT_OT_add_asset_object,
    NODES_OT_add_asset_node,
    NODES_OT_asset_operator,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
