from .face import Face
from pathlib import Path

class Validator:
    """
    Validates user inputs and cube configuration data for the Rubik's Cube application.

    This includes validating rotation key commands, JSON file paths and contents,
    and ensuring the cube's face data structure and colors are correct.
    """

    allowed_color_keys = ["r", "o", "g", "b", "w", "y"]
    allowed_rotation_keys = ["l", "u", "r", "d"]
    allowed_clockwise_keys = ["y", "n"]

    @classmethod
    def validate_keys(cls, keys: tuple[str, str, str]) -> None:
        """
        Validate a rotation command composed of three keys.

        Args:
            keys: Tuple of (observed_face_key, rotated_face_key, clockwise_key).
                  - observed_face_key: Color key of the face being observed ('r','o','g','b','w','y').
                  - rotated_face_key: Rotation direction key relative to observed face ('l','u','r','d').
                  - clockwise_key: 'y' for clockwise, 'n' for counter-clockwise.

        Raises:
            ValueError: If any key is not in the allowed set.
        """
        observed_face_key, rotated_face_key, clockwise_key = keys
        if observed_face_key not in cls.allowed_color_keys:
            raise ValueError("Incorrect value of main face key!")
        if rotated_face_key not in cls.allowed_rotation_keys:
            raise ValueError("Incorrect value of rotated face key!")
        if clockwise_key not in cls.allowed_clockwise_keys:
            raise ValueError("Incorrect value of rotated face key!")

    @staticmethod
    def validate_file_data(faces: dict[str, list[list[str]]]) -> None:
        """
        Validate the structure and content of cube face data loaded from JSON.

        Args:
            faces: Dictionary mapping face names ('red','orange',...) to 3x3 matrices of color keys.

        Calls:
            _validate_data_structure: Ensures six faces, correct matrix dimensions.
            _validate_center_colors: Checks each face's center matches its key.
            _validate_allowed_colors: Ensures all keys are valid color keys.
        """
        Validator._validate_data_structure(faces)
        Validator._validate_center_colors(faces)
        Validator._validate_allowed_colors(faces)

    @staticmethod
    def validate_file_path(file_path: Path) -> None:
        """
        Validate a file path for loading JSON cube data.

        Args:
            file_path: Path object to the JSON file.

        Calls:
            _validate_file_exists: Ensures the file exists.
            _validate_file_extension: Ensures the file has a .json extension.
        """
        Validator._validate_file_exists(file_path)
        Validator._validate_file_extension(file_path)

    @staticmethod
    def _validate_file_extension(file_path: Path) -> None:
        """
        Ensure the file path ends with the .json extension.

        Args:
            file_path: Path to validate.

        Raises:
            ValueError: If file extension is not .json.
        """
        if file_path.suffix != ".json":
            raise ValueError("Only .json format is permitted!")

    @staticmethod
    def _validate_file_exists(file_path: Path) -> None:
        """
        Ensure the file exists at the given path.

        Args:
            file_path: Path to the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def _validate_data_structure(faces: dict[str, list[list[str]]]) -> None:
        """
        Validate the dimensions of the faces data structure.

        Args:
            faces: Dict mapping face names to 3x3 color key matrices.

        Raises:
            ValueError: If there are not exactly 6 faces, or any matrix is not 3x3.
        """
        if len(faces) != 6:
            raise ValueError("Cube must contain 6 faces!")
        for matrix in faces.values():
            if len(matrix) != Face.edge_len:
                raise ValueError("Incorrect row amount!")
            for row in matrix:
                if len(row) != Face.edge_len:
                    raise ValueError("Incorrect column amount!")

    @staticmethod
    def _validate_center_colors(faces: dict[str, list[list[str]]]) -> None:
        """
        Ensure each face's center cell matches the expected color key.

        Args:
            faces: Dict mapping face names ('red', 'orange', etc.) to color key matrices.

        Raises:
            ValueError: If any center cell does not match its face key.
        """
        key_color_map = {
            "red": "r",
            "orange": "o",
            "green": "g",
            "blue": "b",
            "white": "w",
            "yellow": "y",
        }
        for face_color, key in key_color_map.items():
            if faces[face_color][1][1] != key:
                raise ValueError("Center color must match the face color!")

    @classmethod
    def _validate_allowed_colors(cls, faces: dict[str, list[list[str]]]) -> None:
        """
        Ensure all cells in all faces use allowed color keys.

        Args:
            faces: Dict mapping face names to matrices of color keys.

        Raises:
            ValueError: If any color key is not recognized.
        """
        if not all(
            cell in cls.allowed_color_keys
            for matrix in faces.values()
            for row in matrix
            for cell in row
        ):
            raise ValueError("Incorrect key value!")
