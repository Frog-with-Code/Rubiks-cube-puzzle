import json
from pathlib import Path

from .colors import FaceColors
from .cube import Cube
from .face import Face
from .validator import Validator


class CubeController:
    """
    Manages creation and manipulation of Cube objects through high-level operations.

    This includes generating a solved cube, loading cube state from JSON files,
    and parsing user key commands into cube face rotations.
    """

    data_dir = Path("src/rubiks_cube/")
    _color_keys_to_enum = {
        "r": FaceColors.RED,
        "o": FaceColors.ORANGE,
        "g": FaceColors.GREEN,
        "b": FaceColors.BLUE,
        "w": FaceColors.WHITE,
        "y": FaceColors.YELLOW,
    }

    @staticmethod
    def create_solved_cube() -> Cube:
        """
        Create a new solved Cube instance.

        Returns:
            A Cube with each face initialized to its uniform center color:
            red, orange, green, blue, white, yellow.
        """
        return Cube((
            Face(FaceColors.RED),
            Face(FaceColors.ORANGE),
            Face(FaceColors.GREEN),
            Face(FaceColors.BLUE),
            Face(FaceColors.WHITE),
            Face(FaceColors.YELLOW),
        ))

    @classmethod
    def create_cube_from_file(cls, file_name: str, file_dir: str = None) -> Cube:
        """
        Load cube face colors from a JSON file and construct a Cube.

        Args:
            file_name: Name of the JSON file containing cube face data.
            file_dir: Directory path where file is located. Defaults to data_dir.

        The JSON file must have a top-level "faces" object mapping face keys to
        3x3 lists of color keys ("r","o","g","b","w","y").

        Returns:
            A Cube instance with faces colored according to the file.

        Raises:
            ValidatorError: If the file path or data format is invalid.
        """
        if file_dir is None:
            file_dir = cls.data_dir
        full_path = file_dir / file_name
        Validator.validate_file_path(full_path)

        with open(full_path) as f:
            faces_data = json.load(f)["faces"]

        faces_keys = list(faces_data.values())
        Validator.validate_file_data(faces_data)

        enum_matrixes = cls._convert_key_matrix(faces_keys)
        converted_faces = [Face(matrix) for matrix in enum_matrixes]
        return Cube(converted_faces)

    @classmethod
    def _convert_key_matrix(
        cls, key_matrixes: list[list[list[str]]]
    ) -> list[list[list[FaceColors]]]:
        """
        Convert matrices of color keys to matrices of FaceColors enums.

        Args:
            key_matrixes: List of six 3x3 lists of string color keys.

        Returns:
            List of six 3x3 lists of FaceColors enums.
        """
        return [
            [[cls._color_keys_to_enum[cell] for cell in row] for row in matrix]
            for matrix in key_matrixes
        ]

    @staticmethod
    def convert_keys(cube_obj: Cube, keys: tuple[str, str, str]) -> tuple[Face, bool]:
        """
        Parse a triple of user keys into a face rotation command.

        Args:
            cube_obj: Cube on which to perform the rotation.
            keys: Tuple of three strings: (observed_face, neighbor_face, clockwise_flag).
                  Face keys: 'r','o','g','b','w','y'. Clockwise flag: 'y' for clockwise.

        Returns:
            A tuple containing:
                - The Face object to rotate.
                - A boolean indicating rotation direction (True=clockwise).

        Raises:
            ValidatorError: If keys are invalid or not recognized.
        """
        formatted_keys = tuple(key.strip().lower() for key in keys)
        Validator.validate_keys(formatted_keys)

        observed_face_key, rotated_face_key, clockwise_key = formatted_keys
        observed_face = cube_obj.get_face_by_key(observed_face_key)
        rotated_face = observed_face.get_neighbor_by_key(rotated_face_key)
        clockwise = clockwise_key == "y"

        return rotated_face, clockwise