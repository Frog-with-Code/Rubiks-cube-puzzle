from .face import Face
from .colors import FaceColors
import random
import json
from pathlib import Path


class Cube:
    allowed_color_keys = ["r", "o", "g", "b", "w", "y"]
    allowed_rotation_keys = ["l", "u", "r", "d"]
    allowed_clockwise_keys = ["y", "n"]
    data_dir = Path("src/rubiks_cube/")

    @classmethod
    def check_keys(cls, keys):
        main_face_key, rotated_face_key, clockwise_key = keys
        if main_face_key not in cls.allowed_color_keys:
            raise ValueError("Incorrect value of main face key!")
        if rotated_face_key not in cls.allowed_rotation_keys:
            raise ValueError("Incorrect value of rotated face key!")
        if clockwise_key not in cls.allowed_clockwise_keys:
            raise ValueError("Incorrect value of rotated face key!")

    @classmethod
    def create_solved(cls):
        return cls(
            (
                Face(FaceColors.RED),
                Face(FaceColors.ORANGE),
                Face(FaceColors.GREEN),
                Face(FaceColors.BLUE),
                Face(FaceColors.WHITE),
                Face(FaceColors.YELLOW),
            )
        )

    @classmethod
    def create_from_file(cls, file_name, file_dir=None):
        if file_dir is None:
            file_dir = Cube.data_dir
        full_path = file_dir / file_name

        Cube.validate_file_path(full_path)
        with open(full_path) as f:
            faces = json.load(f)["faces"]

        Cube.validate_file_data(faces)
        return cls(
            (
                Face(Cube._convert_key_matrix(faces["red"])),
                Face(Cube._convert_key_matrix(faces["orange"])),
                Face(Cube._convert_key_matrix(faces["green"])),
                Face(Cube._convert_key_matrix(faces["blue"])),
                Face(Cube._convert_key_matrix(faces["white"])),
                Face(Cube._convert_key_matrix(faces["yellow"])),
            )
        )
        
    @staticmethod
    def validate_file_data(faces):
        Cube.validate_data_structure(faces)
        Cube.validate_center_colors(faces)
        Cube.validate_allowed_colors(faces)

    @staticmethod
    def validate_file_path(file_path):
        Cube.validate_file_exists(file_path)
        Cube.validate_file_extension(file_path)

    @staticmethod
    def _orient_edge(edge, condition):
        return edge[::-1] if condition else edge

    @staticmethod
    def validate_file_extension(file_path):
        if file_path.suffix != ".json":
            raise ValueError("Only .json format is permitted!")

    @staticmethod
    def validate_file_exists(file_path):
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def _convert_key_matrix(key_matrix):
        color_map = {
            "r": FaceColors.RED,
            "o": FaceColors.ORANGE,
            "g": FaceColors.GREEN,
            "b": FaceColors.BLUE,
            "w": FaceColors.WHITE,
            "y": FaceColors.YELLOW,
        }
        return [[color_map[cell] for cell in row] for row in key_matrix]

    @staticmethod
    def validate_data_structure(faces):
        if len(faces) != 6:
            raise ValueError("Cube must contain 6 faces!")
        for matrix in faces.values():
            if len(matrix) != Face.edge_len:
                raise ValueError("Incorrect row amount!")
            for row in matrix:
                if len(row) != Face.edge_len:
                    raise ValueError("Incorrect column amount!")

    @staticmethod
    def validate_center_colors(faces):
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

    @staticmethod
    def validate_allowed_colors(faces):
        for matrix in faces.values():
            for row in matrix:
                for cell in row:
                    if cell not in Cube.allowed_color_keys:
                        raise ValueError("Incorrect key value!")

    def __init__(self, faces):
        # * the name of the face depends on the color of its center
        red_face, orange_face, green_face, blue_face, white_face, yellow_face = faces
        self._red_face = red_face
        self._orange_face = orange_face
        self._green_face = green_face
        self._blue_face = blue_face
        self._white_face = white_face
        self._yellow_face = yellow_face

        self._faces = self._create_face_map()
        self._setup_face_connections()

    def _create_face_map(self):
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
        face_keys = list(self._faces.keys())
        last_move = ()
        while actual_count < target_count and actual_count < max_count:
            actual_count += 1
            key = random.choice(face_keys)
            clockwise = random.choice((True, False))

            if last_move and (key == last_move[0] and clockwise != last_move[1]):
                continue
            else:
                self._faces[key].rotate(clockwise)
                self._rotate_neighbors(self._faces[key], clockwise)
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

    def _convert_keys(self, keys):
        formatted_keys = tuple(key.strip() for key in keys)
        Cube.check_keys(formatted_keys)
        main_face_key, rotated_face_key, clockwise_key = formatted_keys

        main_face = self._faces[main_face_key]
        rotated_face = main_face.get_neighbor_by_key(rotated_face_key)
        clockwise = clockwise_key == 'y'
        return rotated_face, clockwise

    def rotate_face(self, keys):
        rotated_face, clockwise = self._convert_keys(keys)
        rotated_face.rotate(clockwise)
        self._rotate_neighbors(rotated_face, clockwise)

    def is_solved(self):
        for face in self._faces.values():
            if not face.is_uniform():
                return False
        return True
