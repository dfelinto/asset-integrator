# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import os


class OBJECT_OT_add_asset_object(bpy.types.Operator):
    """Add asset object"""
    bl_idname = "object.add_asset_object"
    bl_label = "Add Asset Object"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")
    description: bpy.props.StringProperty(name="Description")

    @classmethod
    def description(cls, context, properties):
        return properties.description

    def execute(self, context):

        file_path = self.filepath
        inner_path = 'Object'
        asset_name = self.id_name

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, asset_name),
            directory=os.path.join(file_path, inner_path),
            filename=asset_name,
            do_reuse_local_id=True,
        )

        bpy.ops.transform.translate(value=context.scene.cursor.location)
        return {'FINISHED'}


class NODES_OT_add_asset_node(bpy.types.Operator):
    """Add node group node"""
    bl_idname = "nodes.add_asset_node"
    bl_label = "Add Asset Node"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")
    description: bpy.props.StringProperty(name="Description")

    @classmethod
    def description(cls, context, properties):
        return properties.description

    def execute(self, context):
        node_group = bpy.data.node_groups.get(self.id_name)

        # Mimic Append (Reuse Data) - check name and library filepath.
        if not (node_group and node_group.library and node_group.library.filepath == self.filepath):
            node_groups_before = [
                node_group for node_group in bpy.data.node_groups]

            file_path = self.filepath
            inner_path = 'NodeTree'
            asset_name = self.id_name

            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, asset_name),
                directory=os.path.join(file_path, inner_path),
                filename=asset_name,
                do_reuse_local_id=True,
            )

            node_groups_after = [
                node_group for node_group in bpy.data.node_groups]

            node_groups_diff = [
                node_group for node_group in node_groups_after if node_group not in node_groups_before]

            if node_groups_diff:
                node_group = node_groups_diff[0]
                node_group.asset_clear()
            else:
                # Nothing to do, it means the data-block was there already, but appended.
                pass

        # Ideally we should unappend the asset if the operator got cancelled.
        # This is not possible at the moment.
        return bpy.ops.node.add_node(
            'INVOKE_DEFAULT',
            type="GeometryNodeGroup",
            use_transform=True,
            settings=[
                {
                    "name": "node_tree",
                    "value": "bpy.data.node_groups['{}']".format(node_group.name),
                }])


class NODES_OT_asset_operator(bpy.types.Operator):
    """Run node group as operator"""
    bl_idname = "nodes.add_asset_operator"
    bl_label = "Add Asset Operator"

    filepath: bpy.props.StringProperty(name="Filepath")
    id_name: bpy.props.StringProperty(name="ID Name")
    description: bpy.props.StringProperty(name="Description")

    @classmethod
    def description(cls, context, properties):
        return properties.description

    def execute(self, context):
        node_groups_before = [
            node_group for node_group in bpy.data.node_groups]

        file_path = self.filepath
        inner_path = 'NodeTree'
        asset_name = self.id_name

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, asset_name),
            directory=os.path.join(file_path, inner_path),
            filename=asset_name,
            do_reuse_local_id=True,
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
