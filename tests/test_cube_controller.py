import json
from rubiks_cube import CubeController, FaceColors
import pytest


class TestCubeController:
    def test_create_solved_cube(self):
        cube = CubeController.create_solved_cube()
        expected_colors = [
            FaceColors.RED,
            FaceColors.ORANGE,
            FaceColors.GREEN,
            FaceColors.BLUE,
            FaceColors.WHITE,
            FaceColors.YELLOW,
        ]
        for face, expected_color in zip(
            list(cube._faces_dict.values()), expected_colors
        ):
            assert all(
                cell == expected_color for row in face.get_face_matrix() for cell in row
            )

    def test_create_cube_from_file(self, tmp_path):
        data = {
            "faces": {
                "red": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
                "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
                "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
                "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
            }
        }
        file = tmp_path / "cube.json"
        file.write_text(json.dumps(data))

        cube = CubeController.create_cube_from_file("cube.json", file_dir=tmp_path)

        faces = cube._faces_dict
        assert faces["r"].get_face_matrix() == [[FaceColors.RED] * 3 for _ in range(3)]
        assert faces["o"].get_face_matrix() == [
            [FaceColors.ORANGE] * 3 for _ in range(3)
        ]
        assert faces["g"].get_face_matrix() == [
            [FaceColors.GREEN] * 3 for _ in range(3)
        ]
        assert faces["b"].get_face_matrix() == [[FaceColors.BLUE] * 3 for _ in range(3)]
        assert faces["w"].get_face_matrix() == [
            [FaceColors.WHITE] * 3 for _ in range(3)
        ]
        assert faces["y"].get_face_matrix() == [
            [FaceColors.YELLOW] * 3 for _ in range(3)
        ]

    @pytest.mark.parametrize(
        "keys, expected_face_name, expected_flag",
        [
            (("g", "r", "y"), "red_face", True),
            (("r", "u", "n"), "white_face", False),
            ((" Y ", " D ", "  Y"), "green_face", True),
        ],
    )
    def test_key_conversion(self, keys, expected_face_name, expected_flag):
        cube = CubeController.create_solved_cube()
        expected_face = getattr(cube, f"_{expected_face_name}")
        result = CubeController.convert_keys(cube, keys)
        assert result == (expected_face, expected_flag)
