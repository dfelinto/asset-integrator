# Hardcoded values, to be replaced by data from the API

library_furniture = {
    'Furniture': {
        'Chair': {
            'filepath': "Furniture/furniture.blend",
            'type': 'OBJECT',
        },
        'Table': {
            'filepath': "Furniture/furniture.blend",
            'type': 'COLLECTION',
        }
    },
}

library_human_basemesh = {
    'Mesh':
    {
        'Human Basemesh':
        {
            'Eye': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Foot': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Hand': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Jaw': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Stylized Female': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Stylized Head': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
            'Stylized Male': {
                'filepath': "Human Basemeshes/human_base_meshes.blend",
                'type': 'OBJECT',
            },
        },
    },
}

library_parametric_primitives = {
    'Mesh':
    {
        'Parametric': {
            'Cone': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a cone, edit it in the modifier'
            },
            'Cube': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a cube, edit it in the modifier'

            },
            'Cylinder': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a cylinder, edit it in the modifier'
            },
            'Grid': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a grid, edit it in the modifier'
            },
            'Icosphere': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add an icosphere, edit it in the modifier'
            },
            'UV Sphere': {
                'filepath': "Parametric Primitives/Parametric Primitives.blend",
                'type': 'OBJECT',
                'description': 'Add a uv sphere, edit it in the modifier'

            },
        },
    }
}

library_hair_operators = {
    'Delete':
    {
        'Delete Hair': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'description': 'Delete selected curves',
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
    },
    'Noise':
    {
        'Hair Noise': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'description': 'Mess the hair around',
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
        'Hair Noise Proximity': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
    },
    'Utilities':
    {
        'Hair Thickness': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'description': 'Control the hair thickness',
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
        'Resample': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'description': 'Change the amount of control points for the curves',
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        }
    },
    'Unassigned':
    {
        'Randomize Length': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        }
    }
}

library_hair_operators_extra = {
    'Delete':
    {
        'Delete Random': {
            'filepath': "Geometry Nodes Utils/node_group_operator_test.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
        'Trim': {
            'filepath': "Geometry Nodes Utils/node_group_operator_test.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
    },
    'Noise':
    {
        'Add Noise': {
            'filepath': "Geometry Nodes Utils/node_group_operator_test.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
    },
    'Utilities':
    {
        'Set Radius': {
            'filepath': "Geometry Nodes Utils/node_group_operator_test.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
    },
}

library_mock = {
    'Attribute':
    {
        'Set Hair Attribute': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        }
    },
    'Select': {
        'Odd Hairs': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
        'Even More Hairs': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
    },
    'Curves': {
        'Make Braids': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
        'Make Straight Hair': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
    },
    'View': {
        'View More Hair': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': False,
            'is_operator': True,
        },
        'View Less Hair': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        },
    },
    'New Category':
    {
        'A Node': {
            'filepath': "Geometry Nodes Utils/einar_hair_tools.blend",
            'type': 'NODE_TREE',
            'subtype': 'GEOMETRY_NODES',
            'is_modifier': False,
            'is_node': True,
            'is_operator': True,
        }
    },
}
