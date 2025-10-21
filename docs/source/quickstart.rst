Getting Started
---------------

Quick Start Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from rubiks_cube import CubeController

    # Create a solved cube
    cube = CubeController.create_solved_cube()
    
    # Shuffle the cube
    cube.shuffle(target_count=20)
    
    # Display the cube
    cube.display_all_faces()
    
    # Check if solved
    if cube.is_solved():
        print("Cube is solved!")

Loading from File
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from rubiks_cube import CubeController

    # Load cube state from JSON
    cube = CubeController.create_cube_from_file("my_cube.json")
    cube.display_all_faces()

Rotating Faces
~~~~~~~~~~~~~~

.. code-block:: python

    from rubiks_cube import CubeController

    cube = CubeController.create_solved_cube()
    
    # Rotate the red face clockwise
    red_face = cube.get_face_by_key('r')
    cube.rotate_face(red_face, clockwise=True)
    
    # Or use key conversion
    keys = ('w', 'u', 'y')  # (observed_face, neighbor_direction, clockwise)
    face, direction = CubeController.convert_keys(cube, keys)
    cube.rotate_face(face, direction)