import pytest
from pathlib import Path
from rubiks_cube import Validator

class TestInputValidation:
    @pytest.mark.parametrize(
        "valid_keys",
        [
            ("r", "r", "y"),
            ("o", "d", "n"),
            ("g", "l", "y"),
            ("w", "u", "n"),
        ],
    )
    def test_keys_validation_valid(self, valid_keys):
        Validator.validate_keys(valid_keys)

    @pytest.mark.parametrize(
        "invalid_keys",
        [
            ("r", "r", "r"),
            ("d", "r", "n"),
            ("R", "r", "y"),
            ("Q", "u", "n"),
            ("r", "r", "y", "y"),
        ],
    )
    def test_keys_validation_invalid(self, invalid_keys):
        with pytest.raises(ValueError):
            Validator.validate_keys(invalid_keys)

    @pytest.mark.parametrize(
        "invalid_extensions",
        [
            Path("filename.txt"),
            Path("filename.md"),
            Path("filename.py"),
        ],
    )
    def test_file_extension_validation_invalid(self, invalid_extensions):
        with pytest.raises(ValueError, match="Only .json format is permitted!"):
            Validator._validate_file_extension(invalid_extensions)

    def test_file_extension_validation_valid(self):
        Validator._validate_file_extension(Path("filename.json"))

    @pytest.mark.parametrize(
        "existing_files",
        [
            Path("./tests").resolve() / "test_validation.py",
            Path("./tests") / "test_validation.py",
        ],
    )
    def test_file_existence_validation_valid(self, existing_files):
        Validator._validate_file_exists(existing_files)

    def test_file_existence_validation_invalid(self):
        current_dir = Path("./tests").resolve()
        file_path = current_dir / "not_exist.py"
        with pytest.raises(FileNotFoundError, match=f"File not found: {file_path}"):
            Validator._validate_file_exists(file_path)

    def test_file_path_validation_valid(self):
        current_dir = Path("./src/rubiks_cube").resolve()
        Validator.validate_file_path(current_dir / "input.json")

    def test_file_data_validation_valid(self):
        data = {
            "red": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
            "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
            "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
            "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
            "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
            "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
        }
        Validator.validate_file_data(data)

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {
                "red": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
            },
            {
                "red": [["r", "r", "r"]],
                "orange": [["o", "o", "o"]],
                "green": [["g", "g", "g"]],
                "blue": [["b", "b", "b"]],
                "white": [["w", "w", "w"]],
                "yellow": [["y", "y", "y"]],
            },
            {
                "red": [["r"], ["r"], ["r"]],
                "orange": [["o"], ["o"], ["o"]],
                "green": [["g"], ["g"], ["g"]],
                "blue": [["b"], ["b"], ["b"]],
                "white": [["w"], ["w"], ["w"]],
                "yellow": [["y"], ["y"], ["y"]],
            },
        ],
    )
    def test_data_structure_validation_invalid(self, invalid_data):
        with pytest.raises(ValueError):
            Validator._validate_data_structure(invalid_data)

    def test_center_colors_validation_invalid(self):
        invalid_data = {
            "red": [["r", "r", "r"], ["r", "o", "r"], ["r", "r", "r"]],
            "orange": [["o", "o", "o"], ["o", "r", "o"], ["o", "o", "o"]],
            "green": [["g", "g", "g"], ["g", "b", "g"], ["g", "g", "g"]],
            "blue": [["b", "b", "b"], ["b", "g", "b"], ["b", "b", "b"]],
            "white": [["w", "w", "w"], ["w", "y", "w"], ["w", "w", "w"]],
            "yellow": [["y", "y", "y"], ["y", "r", "y"], ["y", "y", "y"]],
        }
        with pytest.raises(ValueError, match="Center color must match the face color!"):
            Validator._validate_center_colors(invalid_data)

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {
                "red": [["red", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
                "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
                "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
                "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
            },
            {
                "red": [["rr", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
                "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
                "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
                "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
            },
            {
                "red": [["q", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
                "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
                "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
                "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
            },
        ],
    )
    def test_color_validation_invalid(self, invalid_data):
        with pytest.raises(ValueError, match="Incorrect key value!"):
            Validator._validate_allowed_colors(invalid_data)

    def test_face_names_validation_invalid(self):
        invalid_data = {
            "r": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
            "o": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
            "g": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
            "b": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
            "w": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
            "y": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
        }
        with pytest.raises(KeyError):
            Validator._validate_center_colors(invalid_data)