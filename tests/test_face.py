from rubiks_cube import Face, FaceColors, CubeController
import pytest


class TestFace:
    def test_get_row_returns_copy(self):
        face = Face(FaceColors.RED)
        original_row = face._matrix[0]
        returned_row = face.get_row(0)

        assert returned_row == original_row
        assert returned_row is not original_row

        returned_row[0] = FaceColors.BLUE
        assert face.get_row(0)[0] == FaceColors.RED

    def test_set_row_uses_copy(self):
        face = Face(FaceColors.RED)
        external_row = [FaceColors.GREEN, FaceColors.GREEN, FaceColors.GREEN]
        face.set_row(0, external_row)

        assert face.get_row(0) == external_row
        assert face.get_row(0) is not external_row

        external_row[0] = FaceColors.BLUE
        assert face.get_row(0)[0] == FaceColors.GREEN

    def test_get_col_returns_copy(self):
        face = Face(FaceColors.RED)
        returned_col = face.get_row(0)

        returned_col[0] = FaceColors.BLUE
        assert face.get_col(0)[0] == FaceColors.RED

    def test_set_col_uses_copy(self):
        face = Face(FaceColors.RED)
        external_col = [FaceColors.GREEN, FaceColors.GREEN, FaceColors.GREEN]
        face.set_col(0, external_col)

        assert face.get_col(0) == external_col
        assert face.get_col(0) is not external_col

        external_col[0] = FaceColors.BLUE
        assert face.get_col(0)[0] == FaceColors.GREEN

    def test_face_is_uniform(self):
        face = Face(FaceColors.RED)
        assert face.is_uniform() is True

    def test_face_is_not_uniform(self):
        face = Face(FaceColors.RED)
        external_row = [FaceColors.GREEN, FaceColors.GREEN, FaceColors.GREEN]
        face.set_row(0, external_row)
        assert face.is_uniform() is False

    def test_get_face_matrix_returns_copy(self):
        face = Face(FaceColors.RED)
        matrix = face.get_face_matrix()

        assert matrix[0] == face.get_row(0)
        assert matrix[1] == face.get_row(1)
        assert matrix[2] == face.get_row(2)

        matrix[0] = [FaceColors.BLUE, FaceColors.BLUE, FaceColors.BLUE]
        assert face.get_row(0) == [FaceColors.RED, FaceColors.RED, FaceColors.RED]
        matrix[1][0] = FaceColors.BLUE
        assert face.get_row(1) == [FaceColors.RED, FaceColors.RED, FaceColors.RED]

    def test_get_original_neighbor_by_valid_key(self):
        cube = CubeController.create_solved_cube()
        red_face = cube._get_face_by_key("r")
        green_face = cube._get_face_by_key("g")
        blue_face = cube._get_face_by_key("b")
        white_face = cube._get_face_by_key("w")
        yellow_face = cube._get_face_by_key("y")

        assert red_face.get_neighbor_by_key("l") is green_face
        assert red_face.get_neighbor_by_key("r") is blue_face
        assert red_face.get_neighbor_by_key("u") is white_face
        assert red_face.get_neighbor_by_key("d") is yellow_face

    def test_get_original_neighbor_by_invalid_key(self):
        face = Face(FaceColors.RED)
        with pytest.raises(KeyError, match="Invalid neighbor key: q"):
            face.get_neighbor_by_key("q")

    def test_rotation_clockwise(self):
        face = Face(
            [
                [FaceColors.RED, FaceColors.GREEN, FaceColors.BLUE],
                [FaceColors.WHITE, FaceColors.RED, FaceColors.ORANGE],
                [FaceColors.YELLOW, FaceColors.BLUE, FaceColors.GREEN],
            ]
        )
        face.rotate()

        expected = [
            [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
            [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
            [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
        ]
        assert face.get_face_matrix() == expected

    def test_rotation_counterclockwise(self):
        face = Face(
            [
                [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
                [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
                [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
            ]
        )
        face.rotate(False)

        expected = [
            [FaceColors.RED, FaceColors.GREEN, FaceColors.BLUE],
            [FaceColors.WHITE, FaceColors.RED, FaceColors.ORANGE],
            [FaceColors.YELLOW, FaceColors.BLUE, FaceColors.GREEN],
        ]
        assert face.get_face_matrix() == expected

    def test_cycle_rotation(self):
        base_matrix = [
            [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
            [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
            [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
        ]
        rotated_face = Face(
            [
                [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
                [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
                [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
            ]
        )

        rotated_face.rotate()
        rotated_face.rotate()
        rotated_face.rotate()
        rotated_face.rotate()

        assert base_matrix == rotated_face.get_face_matrix()
        
    def test_opposite_rotation(self):
        base_matrix = [
            [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
            [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
            [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
        ]
        rotated_face = Face(
            [
                [FaceColors.YELLOW, FaceColors.WHITE, FaceColors.RED],
                [FaceColors.BLUE, FaceColors.RED, FaceColors.GREEN],
                [FaceColors.GREEN, FaceColors.ORANGE, FaceColors.BLUE],
            ]
        )
        
        rotated_face.rotate(True)
        rotated_face.rotate(False)

        assert base_matrix == rotated_face.get_face_matrix()