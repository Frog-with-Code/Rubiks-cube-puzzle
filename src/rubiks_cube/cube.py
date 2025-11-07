from .face import Face
from .colors import FaceColors
import random


class Cube:
    """
    Represents a standard 3x3 Rubik's Cube composed of six faces.

    Each face is represented by a Face object with an associated center color.
    Cube methods allow rotating faces, shuffling, checking solved state, and
    displaying the cube in the console.
    """

    @staticmethod
    def _orient_edge(edge: list[FaceColors], condition: bool) -> list[FaceColors]:
        """
        Reverse an edge slice if a given condition is True.

        Args:
            edge: List of FaceColors representing one edge of a face.
            condition: Whether to reverse the order of the edge.

        Returns:
            A list of FaceColors, reversed if condition is True, otherwise unchanged.
        """
        return edge[::-1] if condition else edge

    def __init__(self, faces: tuple[Face, Face, Face, Face, Face, Face]) -> None:
        """
        Initialize the Cube with six Face instances.

        The faces must be provided in the order:
        (red_face, orange_face, green_face, blue_face, white_face, yellow_face).

        Args:
            faces: Tuple of six Face objects corresponding to each cube face.
        """
        red_face, orange_face, green_face, blue_face, white_face, yellow_face = faces
        self._red_face = red_face
        self._orange_face = orange_face
        self._green_face = green_face
        self._blue_face = blue_face
        self._white_face = white_face
        self._yellow_face = yellow_face

        self._faces_dict = self._create_face_dict()
        self._setup_face_connections()

    def _create_face_dict(self) -> dict[str, Face]:
        """
        Build a dictionary mapping face keys to Face objects.

        Keys are:
            'r': red, 'o': orange, 'g': green,
            'b': blue, 'w': white,  'y': yellow

        Returns:
            A dict mapping single-character keys to Face instances.
        """
        return {
            "r": self._red_face,
            "o": self._orange_face,
            "g": self._green_face,
            "b": self._blue_face,
            "w": self._white_face,
            "y": self._yellow_face,
        }

    def shuffle(self, target_count: int = 35, max_count: int = 100) -> None:
        """
        Perform a random sequence of face rotations to shuffle the cube.

        Args:
            target_count: Desired number of random moves (default 35).
            max_count: Hard limit on moves to avoid infinite loops (default 100).

        The method avoids immediate inverse moves on the same face.
        """
        good_move_count = 0
        attempts = 0
        face_keys = list(self._faces_dict.keys())
        last_move: tuple[str, bool] = ()

        while good_move_count < target_count and attempts < max_count:
            attempts += 1
            key = random.choice(face_keys)
            clockwise = random.choice((True, False))
            if last_move and (key == last_move[0] and clockwise != last_move[1]):
                continue
            self.rotate_face(self._faces_dict[key], clockwise)
            last_move = (key, clockwise)
            good_move_count += 1

    def _setup_face_connections(self) -> None:
        """
        Configure neighbor dependencies for each face.

        Each face's set_dependency() is called with the four adjacent faces
        in order: left, right, top, bottom.
        """
        self._red_face.set_dependency(
            self._green_face, self._blue_face, self._white_face, self._yellow_face
        )
        self._orange_face.set_dependency(
            self._blue_face, self._green_face, self._white_face, self._yellow_face
        )
        self._green_face.set_dependency(
            self._orange_face, self._red_face, self._white_face, self._yellow_face
        )
        self._blue_face.set_dependency(
            self._red_face, self._orange_face, self._white_face, self._yellow_face
        )
        self._white_face.set_dependency(
            self._orange_face, self._red_face, self._blue_face, self._green_face
        )
        self._yellow_face.set_dependency(
            self._red_face, self._orange_face, self._blue_face, self._green_face
        )

    def _rotate_edge_surface(
        self,
        edge_surface: tuple[
            list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]
        ],
        rotated_face: Face,
        clockwise: bool,
    ) -> tuple[list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]]:
        """
        Rotate the tuple of four edge slices based on face rotation direction.

        Orange, Blue, and Yellow faces invert the rotation direction due to
        extraction order.

        Args:
            edge_surface: Tuple of four lists of FaceColors (edges of adjacent faces).
            rotated_face: The Face object being rotated.
            clockwise: Direction of rotation on the rotated face.

        Returns:
            A tuple of four edge lists, rotated by one position.
        """
        equator_clockwise = (
            not clockwise
            if rotated_face in (self._orange_face, self._blue_face, self._yellow_face)
            else clockwise
        )
        if equator_clockwise:
            return edge_surface[-1:] + edge_surface[:-1]
        return edge_surface[1:] + edge_surface[:1]

    def _get_red_orange_equator(
        self, rotated_face: Face
    ) -> tuple[list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]]:
        """
        Extract the four edge slices around the red or orange face.

        Args:
            rotated_face: Either the red_face or orange_face.

        Returns:
            Tuple of edges from green, white, blue, and yellow faces.
        """
        i, j = (-1, 0) if rotated_face == self._red_face else (0, -1)
        return (
            self._green_face.get_col(i),
            self._white_face.get_col(i),
            self._blue_face.get_col(j),
            self._yellow_face.get_col(j),
        )

    def _get_green_blue_equator(
        self, rotated_face: Face
    ) -> tuple[list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]]:
        """
        Extract the four edge slices around the green or blue face.

        Args:
            rotated_face: Either the green_face or blue_face.

        Returns:
            Tuple of edges from orange, white, red, and yellow faces.
        """
        i, j = (-1, 0) if rotated_face == self._green_face else (0, -1)
        return (
            self._orange_face.get_col(i),
            self._white_face.get_row(i),
            self._red_face.get_col(j),
            self._yellow_face.get_row(i),
        )

    def _get_white_yellow_equator(
        self, rotated_face: Face
    ) -> tuple[list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]]:
        """
        Extract the four edge slices around the white or yellow face.

        Args:
            rotated_face: Either the white_face or yellow_face.

        Returns:
            Tuple of edges from green, orange, blue, and red faces.
        """
        i = 0 if rotated_face == self._white_face else -1
        return (
            self._green_face.get_row(i),
            self._orange_face.get_row(i),
            self._blue_face.get_row(i),
            self._red_face.get_row(i),
        )

    def _get_edge_surface(
        self, rotated_face: Face
    ) -> tuple[list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]]:
        """
        Dispatch to the appropriate equator getter based on rotated face.

        Args:
            rotated_face: The Face object being rotated.

        Returns:
            Tuple of four edge lists from the relevant equator.
        """
        if rotated_face in (self._red_face, self._orange_face):
            return self._get_red_orange_equator(rotated_face)
        if rotated_face in (self._green_face, self._blue_face):
            return self._get_green_blue_equator(rotated_face)
        return self._get_white_yellow_equator(rotated_face)

    def _set_red_orange_equator(
        self,
        edge_surface: tuple[
            list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]
        ],
        rotated_face: Face,
        clockwise: bool,
    ) -> None:
        """
        Place rotated edge slices back onto the green, white, blue, and yellow faces
        after rotating the red or orange face.

        Args:
            edge_surface: Rotated tuple of four edge lists.
            rotated_face: The red_face or orange_face.
            clockwise: Direction of the original rotation.
        """
        i, j = (-1, 0) if rotated_face == self._red_face else (0, -1)
        edge_for_green, edge_for_white, edge_for_blue, edge_for_yellow = edge_surface
        is_red = rotated_face == self._red_face
        orient_condition = is_red == clockwise

        final_edge_for_green = Cube._orient_edge(edge_for_green, orient_condition)
        final_edge_for_blue = Cube._orient_edge(edge_for_blue, orient_condition)
        final_edge_for_white = Cube._orient_edge(edge_for_white, not orient_condition)
        final_edge_for_yellow = Cube._orient_edge(edge_for_yellow, not orient_condition)

        self._green_face.set_col(i, final_edge_for_green)
        self._white_face.set_col(i, final_edge_for_white)
        self._blue_face.set_col(j, final_edge_for_blue)
        self._yellow_face.set_col(j, final_edge_for_yellow)

    def _set_green_blue_equator(
        self,
        edge_surface: tuple[
            list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]
        ],
        rotated_face: Face,
        clockwise: bool,
    ) -> None:
        """
        Place rotated edge slices back onto the orange, white, red, and yellow faces
        after rotating the green or blue face.

        Args:
            edge_surface: Rotated tuple of four edge lists.
            rotated_face: The green_face or blue_face.
            clockwise: Direction of the original rotation.
        """
        i, j = (-1, 0) if rotated_face == self._green_face else (0, -1)
        edge_for_orange, edge_for_white, edge_for_red, edge_for_yellow = edge_surface
        is_green = rotated_face == self._green_face
        orient_condition = is_green == clockwise

        final_edge_for_orange = Cube._orient_edge(edge_for_orange, orient_condition)
        final_edge_for_red = Cube._orient_edge(edge_for_red, orient_condition)
        final_edge_for_white = Cube._orient_edge(edge_for_white, not orient_condition)
        final_edge_for_yellow = Cube._orient_edge(edge_for_yellow, not orient_condition)

        self._orange_face.set_col(i, final_edge_for_orange)
        self._white_face.set_row(i, final_edge_for_white)
        self._red_face.set_col(j, final_edge_for_red)
        self._yellow_face.set_row(i, final_edge_for_yellow)

    def _set_white_yellow_equator(
        self,
        edge_surface: tuple[
            list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]
        ],
        rotated_face: Face,
    ) -> None:
        """
        Place rotated edge slices back onto the four side faces after rotating
        the white or yellow face.

        Args:
            edge_surface: Tuple of four edge lists from green, orange, blue, red.
            rotated_face: The white_face or yellow_face.
        """
        i = 0 if rotated_face == self._white_face else -1
        edge_for_green, edge_for_orange, edge_for_blue, edge_for_red = edge_surface

        self._green_face.set_row(i, edge_for_green)
        self._orange_face.set_row(i, edge_for_orange)
        self._blue_face.set_row(i, edge_for_blue)
        self._red_face.set_row(i, edge_for_red)

    def _set_edge_surface(
        self,
        edge_surface: tuple[
            list[FaceColors], list[FaceColors], list[FaceColors], list[FaceColors]
        ],
        rotated_face: Face,
        clockwise: bool,
    ) -> None:
        """
        Dispatch to the appropriate equator setter based on rotated face.

        Args:
            edge_surface: Rotated tuple of four edge lists.
            rotated_face: The Face object that was rotated.
            clockwise: Rotation direction of that face.
        """
        if rotated_face in (self._red_face, self._orange_face):
            self._set_red_orange_equator(edge_surface, rotated_face, clockwise)
        elif rotated_face in (self._green_face, self._blue_face):
            self._set_green_blue_equator(edge_surface, rotated_face, clockwise)
        else:
            self._set_white_yellow_equator(edge_surface, rotated_face)

    def _rotate_neighbors(self, rotated_face: Face, clockwise: bool) -> None:
        """
        Rotate the edge slices on neighboring faces when one face is rotated.

        Args:
            rotated_face: The Face object being rotated.
            clockwise: Direction of rotation.
        """
        edge_surface = self._get_edge_surface(rotated_face)
        rotated_edge_surface = self._rotate_edge_surface(
            edge_surface, rotated_face, clockwise
        )
        self._set_edge_surface(rotated_edge_surface, rotated_face, clockwise)

    def rotate_face(self, rotated_face: Face, clockwise: bool) -> None:
        """
        Rotate a single face and update its neighbors accordingly.

        Args:
            rotated_face: The Face to rotate.
            clockwise: True for clockwise, False for counter-clockwise.
        """
        rotated_face.rotate(clockwise)
        self._rotate_neighbors(rotated_face, clockwise)

    def is_solved(self) -> bool:
        """
        Check if the cube is in a solved state.

        Returns:
            True if all six faces are uniform in color, False otherwise.
        """
        for face in self._faces_dict.values():
            if not face.is_uniform():
                return False
        return True

    def _get_face_by_key(self, key: str) -> Face:
        """
        Retrieve a Face object by its single-character key.

        Args:
            key: One of 'r', 'o', 'g', 'b', 'w', 'y'.

        Returns:
            The corresponding Face instance.
        """
        return self._faces_dict[key]
