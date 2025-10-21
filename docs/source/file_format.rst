File Format
-----------

Cube states can be saved and loaded using JSON files with the following structure:

.. code-block:: json

    {
      "faces": {
        "red": [
          ["r", "r", "r"],
          ["r", "r", "r"],
          ["r", "r", "r"]
        ],
        "orange": [
          ["o", "o", "o"],
          ["o", "o", "o"],
          ["o", "o", "o"]
        ],
        "green": [
          ["g", "g", "g"],
          ["g", "g", "g"],
          ["g", "g", "g"]
        ],
        "blue": [
          ["b", "b", "b"],
          ["b", "b", "b"],
          ["b", "b", "b"]
        ],
        "white": [
          ["w", "w", "w"],
          ["w", "w", "w"],
          ["w", "w", "w"]
        ],
        "yellow": [
          ["y", "y", "y"],
          ["y", "y", "y"],
          ["y", "y", "y"]
        ]
      }
    }

**Color Key Mapping:**

- ``r``: Red
- ``o``: Orange
- ``g``: Green
- ``b``: Blue
- ``w``: White
- ``y``: Yellow