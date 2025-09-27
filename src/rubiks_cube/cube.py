from face import Face
from colors import FaceColors
import os


class Cube:
    allowed_main_keys = ["r", "o", "g", "b", "w", "y"]
    allowed_rotation_keys = ["l", "u", "r", "d"]
    allowed_clockwise_keys = ["y", "n"]

    @classmethod
    def check_keys(cls, keys):
        main_face_key, rotated_face_key, clockwise_key = keys
        if main_face_key not in cls.allowed_main_keys:
            raise ValueError("Incorrect value of main face key")
        if rotated_face_key not in cls.allowed_rotation_keys:
            raise ValueError("Incorrect value of rotated face key")
        if clockwise_key not in cls.allowed_clockwise_keys:
            raise ValueError("Incorrect value of rotated face key")

    @staticmethod
    def __convert_clockwise_key(clockwise_key):
        return clockwise_key == "y"

    @staticmethod
    def clear_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self):
        # * the name of the face depends on the color of its center
        self.__red_face = Face(FaceColors.RED)
        self.__orange_face = Face(FaceColors.ORANGE)
        self.__green_face = Face(FaceColors.GREEN)
        self.__blue_face = Face(FaceColors.BLUE)
        self.__white_face = Face(FaceColors.WHITE)
        self.__yellow_face = Face(FaceColors.YELLOW)

        self.__faces = {
            "r": self.__red_face,
            "o": self.__orange_face,
            "g": self.__green_face,
            "b": self.__blue_face,
            "y": self.__yellow_face,
            "w": self.__white_face,
        }
        self.__setup_face_connections()

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

        for i in range(row_len):
            for face in self.__faces.values():
                for j in range(col_len):
                    face_matrix = face.get_face_matrix()
                    face_matrix[i][j].draw_square()

                print("   ", end="")
            print("\n")

    def __rotate_edge_surface(self, edge_surface, rotated_face, clockwise):
        # * rotation of orange, blue, yellow faces is inverted
        # * because of order extracting edges
        equator_clockwise = (
            not clockwise
            if rotated_face in (self.__orange_face, self.__blue_face, self.__yellow_face)
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

    def __set_red_orange_equator(self, edge_surface, rotated_face):
        i, j = (-1, 0) if rotated_face == self.__red_face else (0, -1)
        edge_for_green, edge_for_white, edge_for_blue, edge_for_yellow = edge_surface
        self.__green_face.set_col(i, edge_for_green[::-1])
        self.__white_face.set_col(i, edge_for_white)
        self.__blue_face.set_col(j, edge_for_blue[::-1])
        self.__yellow_face.set_col(j, edge_for_yellow)

    def __set_green_blue_equator(self, edge_surface, rotated_face):
        i, j = (-1, 0) if rotated_face == self.__green_face else (0, -1)
        edge_for_orange, edge_for_white, edge_for_red, edge_for_yellow = edge_surface
        self.__orange_face.set_col(i, edge_for_orange[::-1])
        self.__white_face.set_row(i, edge_for_white)
        self.__red_face.set_col(j, edge_for_red[::-1])
        self.__yellow_face.set_row(i, edge_for_yellow)

    def __set_white_yellow_equator(self, edge_surface, rotated_face):
        i = 0 if rotated_face == self.__white_face else -1
        edge_for_green, edge_for_orange, edge_for_blue, edge_for_red = edge_surface
        self.__green_face.set_row(i, edge_for_green)
        self.__orange_face.set_row(i, edge_for_orange)
        self.__blue_face.set_row(i, edge_for_blue)
        self.__red_face.set_row(i, edge_for_red)

    def __set_edge_surface(self, edge_surface, rotated_face):
        if rotated_face in (self.__red_face, self.__orange_face):
            self.__set_red_orange_equator(edge_surface, rotated_face)
        elif rotated_face in (self.__green_face, self.__blue_face):
            self.__set_green_blue_equator(edge_surface, rotated_face)
        else:
            self.__set_white_yellow_equator(edge_surface, rotated_face)

    def __rotate_neighbors(self, rotated_face, clockwise):
        edge_surface = self.__get_edge_surface(rotated_face)
        rotated_edge_surface = self.__rotate_edge_surface(
            edge_surface, rotated_face, clockwise
        )
        self.__set_edge_surface(rotated_edge_surface, rotated_face)

    def rotate_face(self, keys):
        Cube.check_keys(keys)
        main_face_key, rotated_face_key, clockwise_key = keys

        main_face = self.__faces[main_face_key]
        rotated_face = main_face.get_neighbor_by_key(rotated_face_key)
        clockwise = Cube.__convert_clockwise_key(clockwise_key)

        rotated_face.rotate(clockwise)
        self.__rotate_neighbors(rotated_face, clockwise)
