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
                if catalog:
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

    with blendfile.open_blend(filepath) as bf:
        objects = bf.find_blocks_from_code(b'OB')
        for ob in objects:
            asset_data = ob.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            ob_name = ob.get((b'id', b'name'))[2:]
            catalog_name = asset_data.get(b'catalog_simple_name')
            # TODO get proper description
            description = '' # asset_data.get_pointer(b'description')
            uuid = get_uuid_from_object(ob)
            # print('ob_name', ob_name)
            # print("UUID", uuid)

            catalog = catalogs_lookup.get(uuid, catalog_unassigned)
            catalog[ob_name] = {
                'filepath': filepath,
                'description': description,
                'type': 'OBJECT',
            }

        nodes = bf.find_blocks_from_code(b'NT')
        for node in nodes:
            asset_data = node.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            # TODO: do nodes too


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
    uuid = "%8x-%4hx-%4hx-%2hx%2hx-%2hx%2hx%2hx%2hx%2hx%2hx" % (
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


def get_uuid_from_object(ob)-> str:
    """
    Get UUID from object in blendfile
    """
    time_low = ob.get((b'id', b'asset_data', b'catalog_id', b'time_low'))
    time_mid = ob.get((b'id', b'asset_data', b'catalog_id', b'time_mid'))
    time_hi_and_version = ob.get((b'id', b'asset_data', b'catalog_id', b'time_hi_and_version'))
    clock_seq_hi_and_reserved = ob.get((b'id', b'asset_data', b'catalog_id', b'clock_seq_hi_and_reserved'))
    clock_seq_low = ob.get((b'id', b'asset_data', b'catalog_id', b'clock_seq_low'))
    node = ob.get((b'id', b'asset_data', b'catalog_id', b'node'))
    uuid = format_uuid(
        time_low,
        time_mid,
        time_hi_and_version,
        clock_seq_hi_and_reserved,
        clock_seq_low,
        node
        )
    return uuid
