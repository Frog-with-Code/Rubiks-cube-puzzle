from colors import FaceColors


class Face:
    edge_len = 3
    
    def __init__(self, color):
        self.__matrix = [[color] * Face.edge_len for _ in range(Face.edge_len)]

    def set_dependency(self, left_face, right_face, up_face, down_face):
        self.__left_face = left_face
        self.__right_face = right_face
        self.__up_face = up_face
        self.__down_face = down_face

    def rotate_face(self, clockwise=True):
        if clockwise:
            self.__matrix = [list(reversed(col)) for col in zip(*self.__matrix)]
        else:
            self.__matrix = [list(col) for col in zip(*self.__matrix)][::-1]
            
    def get_face(self):
        return [row[:] for row in self.__matrix]

                
