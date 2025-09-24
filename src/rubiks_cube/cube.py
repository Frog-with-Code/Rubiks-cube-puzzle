from face import Face
from colors import FaceColors


class Cube:
    def __init__(self):
        # * the name of the face depends on the color of its center
        self.__red_face = Face(FaceColors.RED)
        self.__orange_face = Face(FaceColors.ORANGE)
        self.__green_face = Face(FaceColors.GREEN)
        self.__blue_face = Face(FaceColors.BLUE)
        self.__white_face = Face(FaceColors.WHITE)
        self.__yellow_face = Face(FaceColors.YELLOW)

        self.__faces = {
            'r': self.__red_face,
            'o': self.__orange_face,
            'g': self.__green_face,
            'b': self.__blue_face,
            'y': self.__yellow_face,
            'w': self.__white_face,
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
            for face in self.__faces.values:
                for j in range(col_len):
                    face_matrix = face.get_face()
                    face_matrix[i][j].draw_square()

                print("   ", end="")
            print("\n")
        print("\n\n")
            
    def __rotate_neighbors(self, rotated_face, clockwise=True):
        edge_surface = (rotated_face.get_neighbor_edges())
        if clockwise:
            rotated_edge_surface = edge_surface[-1:] + edge_surface[:-1]
        else :
            rotated_edge_surface = edge_surface[1:] + edge_surface[:1]
            
        rotated_face.set_neighbor_edges(rotated_edge_surface)
        
    def __get_rotated_face(self, parameter):
        pass
        
            
    def rotate_face(self, parameter, clockwise=True):
        rotated_face = self.__get_rotated_face(parameter)
        rotated_face.rotate(clockwise)
        self.__rotate_neighbors(self.__red_face, clockwise)
        
