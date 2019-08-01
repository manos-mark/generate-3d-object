import bpy
import bmesh
import sys
import os

def parse_arguments():
    # Get arguments from commandline
    argv = sys.argv
    short_arguments = ("-W", "-H", "-D", "-P")
    long_arguments = ("--width", "--height", "--depth", "--pictures-path")
    parsed_arguments = []

    for index, (short, long) in enumerate(zip(short_arguments, long_arguments)):

        arg = None
        if (long in argv):
            if (argv.index(long) + 1 < len(argv)):
                arg = argv[argv.index(long) + 1]
        elif (short in argv):
            if (argv.index(short) + 1 < len(argv)):
                arg = argv[argv.index(short) + 1]

        try:
            if (arg is not None):
                if (short != "-P"):
                    arg = float(arg)
            else:
                raise ValueError
            parsed_arguments.append(arg)
        except ValueError as error:
            print(error)
            print("You must specify a " + long + " argument.\nTry something like: blender --background cube.blend  --python cube.py -- -W 0.48 -H 0.9 -D 0.2 -P ~/Desktop/pictures/")
            sys.exit()

    return parsed_arguments

def main():
    pictures = {
        0: "top.jpg",
        1: "left.jpg",
        2: "bottom.jpg",
        3: "right.jpg",
        4: "front.jpg",
        5: "back.jpg"
    }

    # Parse arguments
    width, height, depth, pictures_path = parse_arguments()

    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Remove everything from scene
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)

    # Create a cube with given dimensions
    bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=True, location=(0, 0, 0))
    bpy.ops.transform.resize(value=(height, width, depth))
    bpy.ops.transform.rotate(axis=(0,90,0))

    # Set variables
    cube = bpy.context.object
    mesh = cube.data
    bm = bmesh.from_edit_mesh(mesh)

    # Iterate through faces
    for index, face in enumerate(bm.faces):
        bpy.ops.mesh.select_all(action='DESELECT')
        if hasattr(bm.faces, "ensure_lookup_table"):
            bm.faces.ensure_lookup_table()
            bm.faces[index].select=True

            # Add material
            material = bpy.data.materials.new(name="Material")
            cube.data.materials.append(material)
            material.preview_render_type = 'CUBE'
            material.use_shadeless = True

            # Add texture
            texture = bpy.data.textures.new(name="Texture", type="IMAGE")
            slot = material.texture_slots.add()
            slot.texture = texture

            # Assign material to face
            bpy.context.object.active_material_index = index
            bpy.ops.object.material_slot_assign()

            # Upload image
            try:
                bpy.ops.image.open(filepath="/"+ pictures[index], directory=pictures_path, files=[{"name": pictures[index]}], relative_path=True, show_multiview=False)
                slot.texture.image = bpy.data.images[pictures[index]]
                image = slot.texture.image
            except:
                raise NameError("Cannot load image %s" % pictures_path+pictures[index])
                sys.exit()

            # Set uploaded image as active image
            for area in bpy.context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = image

            # Unrwap face
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

    # Change view port shade
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')
    space.viewport_shade = 'RENDERED'

    #Export object
    blend_file_path = bpy.data.filepath
    directory = os.path.dirname(blend_file_path)
    target_file = os.path.join(directory, 'cube.obj')
    bpy.ops.export_scene.obj(filepath=target_file)

    print("Done!")

if __name__== "__main__":
    main()
