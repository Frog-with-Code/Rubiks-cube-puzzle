from rubiks_cube import CubeController, CubeFactory, CubeView
import pytest


class TestCubeController:
    @pytest.fixture
    def setup_controller(self):
        cube = CubeFactory().create_solved_cube()
        controller = CubeController(cube)
        return controller, cube

    @pytest.mark.parametrize(
        "keys, expected_face_name, expected_flag",
        [
            (("g", "r", "y"), "red_face", True),
            (("r", "u", "n"), "white_face", False),
            ((" Y ", " D ", "  Y"), "green_face", True),
        ],
    )
    def test_rotate_cube_face_conversion(
        self, setup_controller, keys, expected_face_name, expected_flag
    ):
        controller, cube = setup_controller
        expected_face = getattr(cube, f"_{expected_face_name}")
        
        rotated_face, clockwise = controller._convert_keys(keys)

        assert rotated_face == expected_face
        assert clockwise == expected_flag

    def test_rotate_cube_face_with_invalid_keys_raises_error(self, setup_controller):
        controller, _ = setup_controller

        with pytest.raises(ValueError):
            controller.rotate_cube_face(("x", "y", "z"))
