from .face import Face


class Validator:
    allowed_color_keys = ["r", "o", "g", "b", "w", "y"]
    allowed_rotation_keys = ["l", "u", "r", "d"]
    allowed_clockwise_keys = ["y", "n"]

    @classmethod
    def validate_keys(cls, keys):
        observed_face_key, rotated_face_key, clockwise_key = keys
        if observed_face_key not in cls.allowed_color_keys:
            raise ValueError("Incorrect value of main face key!")
        if rotated_face_key not in cls.allowed_rotation_keys:
            raise ValueError("Incorrect value of rotated face key!")
        if clockwise_key not in cls.allowed_clockwise_keys:
            raise ValueError("Incorrect value of rotated face key!")

    @staticmethod
    def validate_file_data(faces):
        Validator._validate_data_structure(faces)
        Validator._validate_center_colors(faces)
        Validator._validate_allowed_colors(faces)

    @staticmethod
    def validate_file_path(file_path):
        Validator._validate_file_exists(file_path)
        Validator._validate_file_extension(file_path)

    @staticmethod
    def _validate_file_extension(file_path):
        if file_path.suffix != ".json":
            raise ValueError("Only .json format is permitted!")

    @staticmethod
    def _validate_file_exists(file_path):
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def _validate_data_structure(faces):
        if len(faces) != 6:
            raise ValueError("Cube must contain 6 faces!")
        for matrix in faces.values():
            if len(matrix) != Face.edge_len:
                raise ValueError("Incorrect row amount!")
            for row in matrix:
                if len(row) != Face.edge_len:
                    raise ValueError("Incorrect column amount!")

    @staticmethod
    def _validate_center_colors(faces):
        key_color_map = {
            "red": "r",
            "orange": "o",
            "green": "g",
            "blue": "b",
            "white": "w",
            "yellow": "y",
        }
        for face_color in key_color_map.keys():
            if faces[face_color][1][1] != key_color_map[face_color]:
                raise ValueError("Center color must match the face color!")

    @classmethod
    def _validate_allowed_colors(cls, faces):
        if not all(
            cell in cls.allowed_color_keys
            for matrix in faces.values()
            for row in matrix
            for cell in row
        ):
            raise ValueError("Incorrect key value!")
