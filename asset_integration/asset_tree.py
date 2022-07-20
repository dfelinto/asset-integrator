from asset_integration import asset_library
import bpy


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


def get_data_from_library(filepath: str) -> dict:
    import os

    blendfiles = []
    for path, subdirs, files in os.walk(filepath):
        for name in files:
            if name.endswith('.blend'):
                blendfiles.append(os.path.join(path, name))

    blend_data_array = []
    for blend_filepath in blendfiles:
        blend_data = get_data_from_blendfile(blend_filepath)
        blend_data_array.append(blend_data)

    return asset_library.merge_asset_libraries(blend_data_array)


def get_data_from_blendfile(filepath: str) -> dict:
    from . import blendfile
    print(filepath)

    data = {}
    with blendfile.open_blend(filepath) as bf:
        objects = bf.find_blocks_from_code(b'OB')
        for ob in objects:
            asset_data = ob.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            catalog_name = asset_data.get(b'catalog_simple_name')
            description = asset_data.get_pointer(b'description')

            # TODO add description too
            #print("catalog", catalog_name)

        nodes = bf.find_blocks_from_code(b'NT')
        for node in nodes:
            asset_data = node.get_pointer((b'id', b'asset_data'))

            if not asset_data:
                continue

            catalog_name = asset_data.get(b'catalog_simple_name')
            print("catalog", catalog_name)

        print(objects)
        print(filepath)

    return {}
