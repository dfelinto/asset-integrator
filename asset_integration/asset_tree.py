from asset_integration import asset_library
import bpy


UNASSIGNED = 'Unassigned'


def generate_asset_tree(asset_tree={}) -> dict:
    """
    Return dictionary of catalogs and assets
    """
    if asset_tree:
        return asset_tree

    from . import asset_library

    asset_tree = {
        'Mesh':
        {
            'Cone': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a cone, edit it in the modifier'
            },
        }
    }

    lib_data_array = []

    preferences = bpy.context.preferences
    for lib in preferences.filepaths.asset_libraries:
        lib_data = get_data_from_library(lib.path)
        lib_data_array.append(lib_data)

    asset_tree = asset_library.merge_asset_libraries(lib_data_array)
    return asset_tree


def catalog_read(filepath: str, catalog_tree: dict, lookup: dict):
    """
    Read catalog file and populate asset_tree with empty dictionary.
    """
    with open(filepath, 'r') as file:
        for line in file.readlines():
            # Crude parsing of "UUID:catalog/path/for/assets:simple catalog name"
            if len(line) < 8:
                continue
            if line.startswith("#") or line.startswith(" ") or line.startswith("VERSION"):
                continue
            uuid, catalog_path, catalog_simple_name = line.split(':')
            catalog_parts = catalog_path.split('/')

            catalog_parent = catalog_tree
            for catalog_name in catalog_parts:
                catalog = catalog_parent.get(catalog_name)
                if catalog is not None:
                    pass
                else:
                    lookup[uuid] = catalog = catalog_parent[catalog_name] = {}
                catalog_parent = catalog


def get_data_from_library(library_path: str) -> dict:
    import os

    asset_tree = {UNASSIGNED: {}}
    catalogs_lookup = {}
    catalog_filepath = os.path.join(library_path, "blender_assets.cats.txt")
    catalog_read(catalog_filepath, asset_tree, catalogs_lookup)

    blendfiles = []
    for path, subdirs, files in os.walk(library_path):
        for name in files:
            if name.endswith('.blend'):
                blendfiles.append(os.path.join(path, name))

    for blend_filepath in blendfiles:
        get_data_from_blendfile(blend_filepath, asset_tree, catalogs_lookup)

    return asset_tree


def get_data_from_blendfile(filepath: str, asset_tree: dict, catalogs_lookup: dict):
    from . import blendfile
    catalog_unassigned = asset_tree.get(UNASSIGNED)

    node_tree_types = {
        -2: 'UNDEFINED',  # NTREE_UNDEFINED
        -1: 'CUSTOM',  # NTREE_CUSTOM
        0: 'SHADER',  # NTREE_SHADER
        1: 'COMPOSITING',  # NTREE_COMPOSIT
        2: 'TEXTURE',  # NTREE_TEXTURE
        3: 'GEOMETRY_NODES',  # NTREE_GEOMETRY
    }

    with blendfile.open_blend(filepath) as bf:
        objects = bf.find_blocks_from_code(b'OB')
        for ob in objects:
            asset_data = ob.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            ob_name = ob.get((b'id', b'name'))[2:]
            description_ptr = asset_data.get_pointer(b'description')
            description = description_ptr.get_raw_data(
                b'char') if description_ptr else ""
            uuid = get_uuid_from_asset_data(asset_data)

            catalog = catalogs_lookup.get(uuid, catalog_unassigned)
            catalog[ob_name] = {
                'filepath': filepath,
                'description': description,
                'type': 'OBJECT',
            }

        node_trees = bf.find_blocks_from_code(b'NT')
        for node_tree in node_trees:
            asset_data = node_tree.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            node_tree_type = node_tree.get(b'type')
            if node_tree_type != 3:  # GEOMETRY
                continue

            node_tree_name = node_tree.get((b'id', b'name'))[2:]
            description_ptr = asset_data.get_pointer(b'description')
            description = description_ptr.get_raw_data(
                b'char') if description_ptr else ""
            uuid = get_uuid_from_asset_data(asset_data)

            catalog = catalogs_lookup.get(uuid, catalog_unassigned)

            catalog[node_tree_name] = {
                'filepath': filepath,
                'description': description,
                'type': 'NODE_TREE',
                'subtype': node_tree_types[node_tree_type],
            }
            if node_tree_types[node_tree_type] == 'GEOMETRY_NODES':
                # TODO: handle tags to get poll
                # For now consider all of the them to be both node and operator
                is_node = True
                is_operator = True

                catalog[node_tree_name].update(
                    {
                        'is_node': is_node,
                        'is_operator': is_operator,
                    }
                )


def format_uuid(
        time_low,
        time_mid,
        time_hi_and_version,
        clock_seq_hi_and_reserved,
        clock_seq_low,
        node: list) -> str:
    """
    Format UUID based on BLI_uuid_format
    """
    uuid = "%08x-%04hx-%04hx-%02hx%02hx-%02hx%02hx%02hx%02hx%02hx%02hx" % (
        time_low,
        time_mid,
        time_hi_and_version,
        clock_seq_hi_and_reserved,
        clock_seq_low,
        node[0],
        node[1],
        node[2],
        node[3],
        node[4],
        node[5],
    )
    return uuid


def uint_32_t(value):
    """
    Workaround for blendfile bug

    https://developer.blender.org/D15508#420325
    """
    if value < -1:
        return value + 2**32
    return value


def uint_16_t(value):
    """
    Workaround for blendfile bug

    Note: unlike the uint_32_t I'm not sure this one is needed.
    """
    if value < -1:
        return value + 2**16
    return value


def get_uuid_from_asset_data(asset_data) -> str:
    """
    Get UUID from object in blendfile
    """
    time_low = uint_32_t(asset_data.get((b'catalog_id', b'time_low')))
    time_mid = uint_16_t(asset_data.get((b'catalog_id', b'time_mid')))
    time_hi_and_version = uint_16_t(asset_data.get(
        (b'catalog_id', b'time_hi_and_version')))
    clock_seq_hi_and_reserved = asset_data.get(
        (b'catalog_id', b'clock_seq_hi_and_reserved'))
    clock_seq_low = asset_data.get((b'catalog_id', b'clock_seq_low'))
    node = asset_data.get((b'catalog_id', b'node'))
    uuid = format_uuid(
        time_low,
        time_mid,
        time_hi_and_version,
        clock_seq_hi_and_reserved,
        clock_seq_low,
        node
    )
    return uuid
