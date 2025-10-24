from .colors import FaceColors


class Face:
    """
    Represents one face of a 3x3 Rubik's Cube, storing its color matrix
    and handling rotations and neighbor dependencies.
    """

    edge_len = 3

    def __init__(self, color_arg: list[list[FaceColors]] | FaceColors):
        """
        Initialize a Face either from a 2D color matrix or a single color.

        Args:
            color_arg: Either a 3x3 list of FaceColors to set custom colors,
                       or a FaceColors value to create a uniform face.
        """
        if isinstance(color_arg, list):
            self._matrix = [row[:] for row in color_arg]
        else:
            self._matrix = [[color_arg] * Face.edge_len for _ in range(Face.edge_len)]

    def set_dependency(
        self,
        left_face: 'Face',
        right_face: 'Face',
        up_face: 'Face',
        down_face: 'Face'
    ) -> None:
        """
        Set adjacent faces for edge rotations when this face turns.

        Args:
            left_face: Face to the left.
            right_face: Face to the right.
            up_face: Face above.
            down_face: Face below.
        """
        self._left_face = left_face
        self._right_face = right_face
        self._up_face = up_face
        self._down_face = down_face

    def rotate(self, clockwise: bool = True) -> None:
        """
        Rotate the face 90 degrees in-place.

        Args:
            clockwise: True for clockwise rotation, False for counter-clockwise.
        """
        if clockwise:
            # Transpose and reverse each row for clockwise rotation
            self._matrix = [list(reversed(col)) for col in zip(*self._matrix)]
        else:
            # Transpose then reverse row order for counter-clockwise rotation
            self._matrix = [list(col) for col in zip(*self._matrix)][::-1]

    def get_face_matrix(self) -> list[list[FaceColors]]:
        """
        Get a deep copy of the face's color matrix.

        Returns:
            A 3x3 list of FaceColors.
        """
        return [row[:] for row in self._matrix]

    def get_neighbor_by_key(self, key: str) -> 'Face':
        """
        Retrieve an adjacent face by direction key.

        Args:
            key: 'l' for left, 'r' for right, 'u' for up, 'd' for down.

        Returns:
            The corresponding Face instance.
        """
        match key:
            case "l":
                return self._left_face
            case "u":
                return self._up_face
            case "r":
                return self._right_face
            case "d":
                return self._down_face
            case _:
                raise KeyError(f"Invalid neighbor key: {key}")

    def get_col(self, index: int) -> list[FaceColors]:
        """
        Extract a column of the face's matrix.

        Args:
            index: Column index (0 to 2).

        Returns:
            A list of three FaceColors from the specified column.
        """
        return [row[index] for row in self._matrix]

    def get_row(self, index: int) -> list[FaceColors]:
        """
        Extract a row of the face's matrix.

        Args:
            index: Row index (0 to 2).

        Returns:
            A list of three FaceColors from the specified row.
        """
        return self._matrix[index][:]

    def set_col(self, index: int, col: list[FaceColors]) -> None:
        """
        Replace a column in the face's matrix.

        Args:
            index: Column index (0 to 2).
            col: List of three FaceColors to set.
        """
        for i, row in enumerate(self._matrix):
            row[index] = col[i]

    def set_row(self, index: int, row: list[FaceColors]) -> None:
        """
        Replace a row in the face's matrix.

        Args:
            index: Row index (0 to 2).
            row: List of three FaceColors to set.
        """
        self._matrix[index] = row[:]

    def is_uniform(self) -> bool:
        """
        Check if all cells on the face are the same color.

        Returns:
            True if every cell matches the center cell, False otherwise.
        """
        center_color = self._matrix[1][1]
        for row in self._matrix:
            for cell in row:
                if cell != center_color:
                    return False
        return True
