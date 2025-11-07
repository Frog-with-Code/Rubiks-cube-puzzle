from rubiks_cube import CubeFactory
import pytest


class TestCube:
    @pytest.fixture
    def setup_factory(self):
        return CubeFactory()
    
    @pytest.mark.parametrize(
        "key, face_name",
        [("r", "_red_face"), ("b", "_blue_face"), ("w", "_white_face")],
    )
    def test_get_original_face_by_key(self, key, face_name, setup_factory):
        factory = setup_factory
        cube = factory.create_solved_cube()
        face = getattr(cube, face_name)
        face_by_key = cube._get_face_by_key(key)

        assert face is face_by_key

    def test_solved_cube(self, setup_factory):
        factory = setup_factory
        cube = factory.create_solved_cube()
        assert cube.is_solved() is True

    def test_unsolved_cube(self, setup_factory):
        factory = setup_factory
        cube = factory.create_solved_cube()
        cube.shuffle(1, 100)
        assert cube.is_solved() is False

    @pytest.mark.parametrize(
        "face_key, clockwise, expected_faces",
        [
            (
                "r",
                True,
                {
                    "red": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                    "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                    "green": [["g", "g", "y"], ["g", "g", "y"], ["g", "g", "y"]],
                    "blue": [["w", "b", "b"], ["w", "b", "b"], ["w", "b", "b"]],
                    "white": [["w", "w", "g"], ["w", "w", "g"], ["w", "w", "g"]],
                    "yellow": [["b", "y", "y"], ["b", "y", "y"], ["b", "y", "y"]],
                },
            ),
            (
                "r",
                False,
                {
                    "red": [["r", "r", "r"], ["r", "r", "r"], ["r", "r", "r"]],
                    "orange": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
                    "green": [["g", "g", "w"], ["g", "g", "w"], ["g", "g", "w"]],
                    "blue": [["y", "b", "b"], ["y", "b", "b"], ["y", "b", "b"]],
                    "white": [["w", "w", "b"], ["w", "w", "b"], ["w", "w", "b"]],
                    "yellow": [["g", "y", "y"], ["g", "y", "y"], ["g", "y", "y"]],
                },
            ),
            (
                "g",
                True,
                {
                    "red": [["w", "r", "r"], ["w", "r", "r"], ["w", "r", "r"]],
                    "orange": [["o", "o", "y"], ["o", "o", "y"], ["o", "o", "y"]],
                    "green": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
                    "blue": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
                    "white": [["w", "w", "w"], ["w", "w", "w"], ["o", "o", "o"]],
                    "yellow": [["y", "y", "y"], ["y", "y", "y"], ["r", "r", "r"]],
                },
            ),
            (
                "w",
                True,
                {
                    "red": [["b", "b", "b"], ["r", "r", "r"], ["r", "r", "r"]],
                    "orange": [["g", "g", "g"], ["o", "o", "o"], ["o", "o", "o"]],
                    "green": [["r", "r", "r"], ["g", "g", "g"], ["g", "g", "g"]],
                    "blue": [["o", "o", "o"], ["b", "b", "b"], ["b", "b", "b"]],
                    "white": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
                    "yellow": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]],
                },
            ),
        ],
    )
    def test_face_rotation(self, face_key, clockwise, expected_faces, setup_factory):
        factory = setup_factory
        cube = factory.create_solved_cube()

        red_face = cube._get_face_by_key("r")
        orange_face = cube._get_face_by_key("o")
        green_face = cube._get_face_by_key("g")
        blue_face = cube._get_face_by_key("b")
        white_face = cube._get_face_by_key("w")
        yellow_face = cube._get_face_by_key("y")
        faces = [
            red_face,
            orange_face,
            green_face,
            blue_face,
            white_face,
            yellow_face,
        ]

        rotated_face = cube._get_face_by_key(face_key)
        cube.rotate_face(rotated_face, clockwise)
        converted_matrixes = setup_factory._convert_key_matrix(
            list(expected_faces.values())
        )

        for actual_matrix, expected_face in zip(converted_matrixes, faces):
            assert actual_matrix == expected_face.get_face_matrix()

    def test_cube_shuffle(self, setup_factory):
        factory = setup_factory
        solved_cube = factory.create_solved_cube()
        cube = factory.create_solved_cube()
        cube.shuffle(35, 100)
        assert (
            all(
                face.get_face_matrix() == solved_face.get_face_matrix()
                for face, solved_face in zip(
                    list(cube._faces_dict.values()),
                    list(solved_cube._faces_dict.values()),
                )
            )
            is False
        )
