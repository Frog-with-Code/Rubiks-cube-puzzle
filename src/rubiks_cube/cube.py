from .face import Face
import random


class Cube:
    @staticmethod
    def _orient_edge(edge, condition):
        return edge[::-1] if condition else edge

    def __init__(self, faces):
        # * the name of the face depends on the color of its center
        red_face, orange_face, green_face, blue_face, white_face, yellow_face = faces
        self._red_face = red_face
        self._orange_face = orange_face
        self._green_face = green_face
        self._blue_face = blue_face
        self._white_face = white_face
        self._yellow_face = yellow_face

        self._faces_dict = self._create_face_dict()
        self._setup_face_connections()

    def _create_face_dict(self):
        return {
            "r": self._red_face,
            "o": self._orange_face,
            "g": self._green_face,
            "b": self._blue_face,
            "y": self._yellow_face,
            "w": self._white_face,
        }

    def shuffle(self, target_count=35, max_count=100):
        actual_count = 0
        face_keys = list(self._faces_dict.keys())
        last_move = ()
        while actual_count < target_count and actual_count < max_count:
            actual_count += 1
            key = random.choice(face_keys)
            clockwise = random.choice((True, False))

            if last_move and (key == last_move[0] and clockwise != last_move[1]):
                continue
            else:
                self._faces_dict[key].rotate(clockwise)
                self._rotate_neighbors(self._faces_dict[key], clockwise)
                last_move = (key, clockwise)

    def _setup_face_connections(self):
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

    def display_all_faces(self):
        row_len = col_len = Face.edge_len
        for row in self._white_face.get_face_matrix():
            print(" " * 15, end="")
            for cell in row:
                cell.draw_square()
            print("\n")

        lateral_space = (
            self._orange_face,
            self._green_face,
            self._red_face,
            self._blue_face,
        )
        for i in range(row_len):
            for face in lateral_space:
                for j in range(col_len):
                    face_matrix = face.get_face_matrix()
                    face_matrix[i][j].draw_square()

                print("   ", end="")
            print("\n")

        for row in self._yellow_face.get_face_matrix()[::-1]:
            print(" " * 15, end="")
            for cell in row[::-1]:
                cell.draw_square()
            print("\n")

    def _rotate_edge_surface(self, edge_surface, rotated_face, clockwise):
        # * rotation of orange, blue, yellow faces is inverted
        # * because of order extracting edges
        equator_clockwise = (
            not clockwise
            if rotated_face in (self._orange_face, self._blue_face, self._yellow_face)
            else clockwise
        )

        if equator_clockwise:
            return edge_surface[-1:] + edge_surface[:-1]
        else:
            return edge_surface[1:] + edge_surface[:1]

    def _get_red_orange_equator(self, rotated_face):
        i, j = (-1, 0) if rotated_face == self._red_face else (0, -1)
        edge_surface = (
            self._green_face.get_col(i),
            self._white_face.get_col(i),
            self._blue_face.get_col(j),
            self._yellow_face.get_col(j),
        )
        return edge_surface

    def _get_green_blue_equator(self, rotated_face):
        i, j = (-1, 0) if rotated_face == self._green_face else (0, -1)
        edge_surface = (
            self._orange_face.get_col(i),
            self._white_face.get_row(i),
            self._red_face.get_col(j),
            self._yellow_face.get_row(i),
        )
        return edge_surface

    def _get_white_yellow_equator(self, rotated_face):
        i = 0 if rotated_face == self._white_face else -1
        edge_surface = (
            self._green_face.get_row(i),
            self._orange_face.get_row(i),
            self._blue_face.get_row(i),
            self._red_face.get_row(i),
        )
        return edge_surface

    def _get_edge_surface(self, rotated_face):
        if rotated_face in (self._red_face, self._orange_face):
            edge_surface = self._get_red_orange_equator(rotated_face)
        elif rotated_face in (self._green_face, self._blue_face):
            edge_surface = self._get_green_blue_equator(rotated_face)
        else:
            edge_surface = self._get_white_yellow_equator(rotated_face)
        return edge_surface

    def _set_red_orange_equator(self, edge_surface, rotated_face, clockwise):
        i, j = (-1, 0) if rotated_face == self._red_face else (0, -1)
        edge_for_green, edge_for_white, edge_for_blue, edge_for_yellow = edge_surface

        # * condition for orienting edge is defined by its position and direction of rotation
        # * 2/4 edges are inverted
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

    def _set_green_blue_equator(self, edge_surface, rotated_face, clockwise):
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

    def _set_white_yellow_equator(self, edge_surface, rotated_face):
        i = 0 if rotated_face == self._white_face else -1
        edge_for_green, edge_for_orange, edge_for_blue, edge_for_red = edge_surface

        self._green_face.set_row(i, edge_for_green)
        self._orange_face.set_row(i, edge_for_orange)
        self._blue_face.set_row(i, edge_for_blue)
        self._red_face.set_row(i, edge_for_red)

    def _set_edge_surface(self, edge_surface, rotated_face, clockwise):
        if rotated_face in (self._red_face, self._orange_face):
            self._set_red_orange_equator(edge_surface, rotated_face, clockwise)
        elif rotated_face in (self._green_face, self._blue_face):
            self._set_green_blue_equator(edge_surface, rotated_face, clockwise)
        else:
            self._set_white_yellow_equator(edge_surface, rotated_face)

    def _rotate_neighbors(self, rotated_face, clockwise):
        edge_surface = self._get_edge_surface(rotated_face)
        rotated_edge_surface = self._rotate_edge_surface(
            edge_surface, rotated_face, clockwise
        )
        self._set_edge_surface(rotated_edge_surface, rotated_face, clockwise)

    def rotate_face(self, rotated_face, clockwise):
        rotated_face.rotate(clockwise)
        self._rotate_neighbors(rotated_face, clockwise)

    def is_solved(self):
        for face in self._faces_dict.values():
            if not face.is_uniform():
                return False
        return True

    def get_face_by_key(self, key):
        return self._faces_dict[key]