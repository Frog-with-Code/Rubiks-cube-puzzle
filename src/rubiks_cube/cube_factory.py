from .cube import Cube
from pathlib import Path
from .colors import FaceColors
from .face import Face
from .validator import Validator
import json


class CubeFactory:
    data_dir = Path("src/rubiks_cube/")
    _color_keys_to_enum = {
        "r": FaceColors.RED,
        "o": FaceColors.ORANGE,
        "g": FaceColors.GREEN,
        "b": FaceColors.BLUE,
        "w": FaceColors.WHITE,
        "y": FaceColors.YELLOW,
    }

    def create_solved_cube(self) -> Cube:
        """
        Create a new solved Cube instance.

        Returns:
            A Cube with each face initialized to its uniform center color:
            red, orange, green, blue, white, yellow.
        """
        return Cube(
            (
                Face(FaceColors.RED),
                Face(FaceColors.ORANGE),
                Face(FaceColors.GREEN),
                Face(FaceColors.BLUE),
                Face(FaceColors.WHITE),
                Face(FaceColors.YELLOW),
            )
        )

    def create_cube_from_file(self, file_name: str, file_dir: str = None) -> Cube:
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
            file_dir = CubeFactory.data_dir
        full_path = file_dir / file_name
        Validator.validate_file_path(full_path)

        with open(full_path) as f:
            faces_data = json.load(f)["faces"]

        faces_keys = list(faces_data.values())
        Validator.validate_file_data(faces_data)

        enum_matrixes = self._convert_key_matrix(faces_keys)
        converted_faces = [Face(matrix) for matrix in enum_matrixes]
        return Cube(converted_faces)

    def _convert_key_matrix(
        self, key_matrixes: list[list[list[str]]]
    ) -> list[list[list[FaceColors]]]:
        """
        Convert matrices of color keys to matrices of FaceColors enums.

        Args:
            key_matrixes: List of six 3x3 lists of string color keys.

        Returns:
            List of six 3x3 lists of FaceColors enums.
        """
        return [
            [[CubeFactory._color_keys_to_enum[cell] for cell in row] for row in matrix]
            for matrix in key_matrixes
        ]
