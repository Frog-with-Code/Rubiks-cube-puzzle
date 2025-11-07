from .cube import Cube
from .face import Face


class CubeView:
    @staticmethod
    def display_cube_state(cube: Cube) -> None:
        """
        Print an unfolded representation of the cube to the console.

        - White face on top
        - Four side faces in the middle row (O, G, R, B)
        - Yellow face on bottom

        Each cell is drawn via its draw_square() method.

        Args:
            cube: Cube instance to print its state
        """
        row_len = col_len = Face.edge_len

        # Top (white)
        for row in cube._white_face.get_face_matrix():
            print(" " * 15, end="")
            for cell in row:
                cell.draw_square()
            print("\n")

        # Middle (orange, green, red, blue)
        lateral_faces = (
            cube._orange_face,
            cube._green_face,
            cube._red_face,
            cube._blue_face,
        )
        for i in range(row_len):
            for face in lateral_faces:
                for j in range(col_len):
                    face.get_face_matrix()[i][j].draw_square()
                print("   ", end="")
            print("\n")

        # Bottom (yellow)
        for row in cube._yellow_face.get_face_matrix()[::-1]:
            print(" " * 15, end="")
            for cell in row[::-1]:
                cell.draw_square()
            print("\n")
