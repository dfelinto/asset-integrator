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
        node_group = bpy.data.node_groups.get(self.id_name)

        # Only re-use data-block if it comes from the correct library
        if node_group and node_group.library:
            if node_group.library.filepath != self.filepath:
                node_group = None

        if not node_group:
            node_group = get_asset_datablock_node_groups(
                self.filepath, self.id_name)

        else:
            bpy.ops.node.add_node(
                type="GeometryNodeGroup",
                use_transform=True,
                settings=[
                    {
                        "name": "node_tree",
                        "value": "bpy.data.node_groups['{}']".format(node_group.name),
                    }])

        return {'FINISHED'}


class NODES_OT_asset_operator(bpy.types.Operator):
    """Run node group as operator"""
    bl_idname = "nodes.add_asset_operator"
    bl_label = "Add Asset Operator"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")

    def execute(self, context):
        node_groups_before = [
            node_group for node_group in bpy.data.node_groups]

        file_path = self.filepath
        inner_path = 'NodeTree'
        asset_name = self.id_name

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, asset_name),
            directory=os.path.join(file_path, inner_path),
            filename=asset_name
        )

        node_groups_after = [node_group for node_group in bpy.data.node_groups]
        if len(node_groups_before) != len(node_groups_after):
            node_group = [
                node_group for node_group in node_groups_after if node_group not in node_groups_before][0]
        else:
            node_group = bpy.data.node_groups.get(self.id_name)

        # Run the curve operator
        bpy.ops.curves.execute_node_group(node_group_name=node_group.name)

        # Cleanup the file afterwards
        bpy.data.node_groups.remove(node_group)

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
