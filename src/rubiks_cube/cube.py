from .face import Face
from .colors import FaceColors
import os
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
        
    @staticmethod
    def validate_file_data(faces):
        Cube.validate_data_structure(faces)
        Cube.validate_center_colors(faces)
        Cube.validate_allowed_colors(faces)
        
    @staticmethod
    def validate_file_path(file_path):
        Cube.validate_file_exists(file_path)
        Cube.validate_file_extension(file_path)

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
    def _convert_clockwise_key(clockwise_key):
        return clockwise_key == "y"

    @staticmethod
    def clear_terminal():
        os.system("cls" if os.name == "nt" else "clear")

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
            'red': 'r',
            'orange': 'o',
            'green': 'g',
            'blue': 'b',
            'white': 'w',
            'yellow': 'y'
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
        self.__red_face = red_face
        self.__orange_face = orange_face
        self.__green_face = green_face
        self.__blue_face = blue_face
        self.__white_face = white_face
        self.__yellow_face = yellow_face

        self.__faces = self.__create_face_map()
        self.__setup_face_connections()

    def __create_face_map(self):
        return {
            "r": self.__red_face,
            "o": self.__orange_face,
            "g": self.__green_face,
            "b": self.__blue_face,
            "y": self.__yellow_face,
            "w": self.__white_face,
        }

    def shuffle(self, target_count=35, max_count=100):
        actual_count = 0
        face_keys = list(self.__faces.keys())
        last_move = ()
        while actual_count < target_count and actual_count < max_count:
            actual_count += 1
            key = random.choice(face_keys)
            clockwise = random.choice((True, False))

            if last_move and (key == last_move[0] and clockwise != last_move[1]):
                continue
            else:
                self.__faces[key].rotate(clockwise)
                self.__rotate_neighbors(self.__faces[key], clockwise)
                last_move = (key, clockwise)

    def __setup_face_connections(self):
        self.__red_face.set_dependency(
            self.__green_face, self.__blue_face, self.__white_face, self.__yellow_face
        )
        self.__orange_face.set_dependency(
            self.__blue_face, self.__green_face, self.__white_face, self.__yellow_face
        )
        self.__green_face.set_dependency(
            self.__orange_face, self.__red_face, self.__white_face, self.__yellow_face
        )
        self.__blue_face.set_dependency(
            self.__red_face, self.__orange_face, self.__white_face, self.__yellow_face
        )
        self.__white_face.set_dependency(
            self.__orange_face, self.__red_face, self.__blue_face, self.__green_face
        )
        self.__yellow_face.set_dependency(
            self.__red_face, self.__orange_face, self.__blue_face, self.__green_face
        )

    def display_all_faces(self):
        row_len = col_len = Face.edge_len
        for row in self.__white_face.get_face_matrix():
            print(' ' * 15, end="")
            for cell in row:
                cell.draw_square()
            print('\n')

        lateral_space = (self.__orange_face, self.__green_face, self.__red_face, self.__blue_face)
        for i in range(row_len):
            for face in lateral_space:
                for j in range(col_len):
                    face_matrix = face.get_face_matrix()
                    face_matrix[i][j].draw_square()

                print("   ", end="")
            print("\n")
            
        for row in self.__yellow_face.get_face_matrix()[::-1]:
            print(' '*15, end="")
            for cell in row[::-1]:
                cell.draw_square()
            print('\n')
                    

    def __rotate_edge_surface(self, edge_surface, rotated_face, clockwise):
        # * rotation of orange, blue, yellow faces is inverted
        # * because of order extracting edges
        equator_clockwise = (
            not clockwise
            if rotated_face
            in (self.__orange_face, self.__blue_face, self.__yellow_face)
            else clockwise
        )

        if equator_clockwise:
            return edge_surface[-1:] + edge_surface[:-1]
        else:
            return edge_surface[1:] + edge_surface[:1]

    def __get_red_orange_equator(self, rotated_face):
        i, j = (-1, 0) if rotated_face == self.__red_face else (0, -1)
        edge_surface = (
            self.__green_face.get_col(i),
            self.__white_face.get_col(i),
            self.__blue_face.get_col(j),
            self.__yellow_face.get_col(j),
        )
        return edge_surface

    def __get_green_blue_equator(self, rotated_face):
        i, j = (-1, 0) if rotated_face == self.__green_face else (0, -1)
        edge_surface = (
            self.__orange_face.get_col(i),
            self.__white_face.get_row(i),
            self.__red_face.get_col(j),
            self.__yellow_face.get_row(i),
        )
        return edge_surface

    def __get_white_yellow_equator(self, rotated_face):
        i = 0 if rotated_face == self.__white_face else -1
        edge_surface = (
            self.__green_face.get_row(i),
            self.__orange_face.get_row(i),
            self.__blue_face.get_row(i),
            self.__red_face.get_row(i),
        )
        return edge_surface

    def __get_edge_surface(self, rotated_face):
        if rotated_face in (self.__red_face, self.__orange_face):
            edge_surface = self.__get_red_orange_equator(rotated_face)
        elif rotated_face in (self.__green_face, self.__blue_face):
            edge_surface = self.__get_green_blue_equator(rotated_face)
        else:
            edge_surface = self.__get_white_yellow_equator(rotated_face)
        return edge_surface

    def __set_red_orange_equator(self, edge_surface, rotated_face, clockwise):
        i, j = (-1, 0) if rotated_face == self.__red_face else (0, -1)
        edge_for_green, edge_for_white, edge_for_blue, edge_for_yellow = edge_surface

        # * condition for orienting edge is defined by its position and direction of rotation
        # * 2/4 edges are inverted
        is_red = rotated_face == self.__red_face
        orient_condition = is_red == clockwise

        final_edge_for_green = Cube._orient_edge(edge_for_green, orient_condition)
        final_edge_for_blue = Cube._orient_edge(edge_for_blue, orient_condition)
        final_edge_for_white = Cube._orient_edge(edge_for_white, not orient_condition)
        final_edge_for_yellow = Cube._orient_edge(
            edge_for_yellow, not orient_condition
        )

        self.__green_face.set_col(i, final_edge_for_green)
        self.__white_face.set_col(i, final_edge_for_white)
        self.__blue_face.set_col(j, final_edge_for_blue)
        self.__yellow_face.set_col(j, final_edge_for_yellow)

    def __set_green_blue_equator(self, edge_surface, rotated_face, clockwise):
        i, j = (-1, 0) if rotated_face == self.__green_face else (0, -1)
        edge_for_orange, edge_for_white, edge_for_red, edge_for_yellow = edge_surface
        is_green = rotated_face == self.__green_face
        orient_condition = is_green == clockwise

        final_edge_for_orange = Cube._orient_edge(edge_for_orange, orient_condition)
        final_edge_for_red = Cube._orient_edge(edge_for_red, orient_condition)
        final_edge_for_white = Cube._orient_edge(edge_for_white, not orient_condition)
        final_edge_for_yellow = Cube._orient_edge(
            edge_for_yellow, not orient_condition
        )

        self.__orange_face.set_col(i, final_edge_for_orange)
        self.__white_face.set_row(i, final_edge_for_white)
        self.__red_face.set_col(j, final_edge_for_red)
        self.__yellow_face.set_row(i, final_edge_for_yellow)

    def __set_white_yellow_equator(self, edge_surface, rotated_face):
        i = 0 if rotated_face == self.__white_face else -1
        edge_for_green, edge_for_orange, edge_for_blue, edge_for_red = edge_surface

        self.__green_face.set_row(i, edge_for_green)
        self.__orange_face.set_row(i, edge_for_orange)
        self.__blue_face.set_row(i, edge_for_blue)
        self.__red_face.set_row(i, edge_for_red)

    def __set_edge_surface(self, edge_surface, rotated_face, clockwise):
        if rotated_face in (self.__red_face, self.__orange_face):
            self.__set_red_orange_equator(edge_surface, rotated_face, clockwise)
        elif rotated_face in (self.__green_face, self.__blue_face):
            self.__set_green_blue_equator(edge_surface, rotated_face, clockwise)
        else:
            self.__set_white_yellow_equator(edge_surface, rotated_face)

    def __rotate_neighbors(self, rotated_face, clockwise):
        edge_surface = self.__get_edge_surface(rotated_face)
        rotated_edge_surface = self.__rotate_edge_surface(
            edge_surface, rotated_face, clockwise
        )
        self.__set_edge_surface(rotated_edge_surface, rotated_face, clockwise)
        
    def __convert_keys(self, keys):
        formatted_keys = tuple(key.strip() for key in keys)
        Cube.check_keys(formatted_keys)
        main_face_key, rotated_face_key, clockwise_key = formatted_keys

        main_face = self.__faces[main_face_key]
        rotated_face = main_face.get_neighbor_by_key(rotated_face_key)
        clockwise = Cube._convert_clockwise_key(clockwise_key)
        return rotated_face, clockwise

    def rotate_face(self, keys):
        rotated_face, clockwise = self.__convert_keys(keys)
        rotated_face.rotate(clockwise)
        self.__rotate_neighbors(rotated_face, clockwise)

    def is_solved(self):
        for face in self.__faces.values():
            if not face.is_uniform():
                return False
        return True
