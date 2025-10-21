from .colors import FaceColors
import json
from pathlib import Path
from .cube import Cube
from .face import Face
from .validator import Validator


class CubeController:
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

    @classmethod
    def create_cube_from_file(cls, file_name: str, file_dir: str = None) -> Cube:
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
        return [
            [[cls._color_keys_to_enum[cell] for cell in row] for row in matrix]
            for matrix in key_matrixes
        ]

    @staticmethod
    def convert_keys(cube_obj: Cube, keys: tuple[str, str, str]) -> tuple[Face, bool]:
        formatted_keys = tuple(key.strip().lower() for key in keys)
        Validator.validate_keys(formatted_keys)
        observed_face_key, rotated_face_key, clockwise_key = formatted_keys

        observed_face = cube_obj.get_face_by_key(observed_face_key)
        rotated_face = observed_face.get_neighbor_by_key(rotated_face_key)
        clockwise = clockwise_key == "y"

        return rotated_face, clockwise
