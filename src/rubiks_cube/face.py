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

    def rotate(self, clockwise):
        if clockwise:
            self.__matrix = [list(reversed(col)) for col in zip(*self.__matrix)]
        else:
            self.__matrix = [list(col) for col in zip(*self.__matrix)][::-1]

    def get_face_matrix(self):
        return [row[:] for row in self.__matrix]

    def get_neighbor_by_key(self, key):
        match key:
            case "l":
                return self.__left_face
            case "u":
                return self.__up_face
            case "r":
                return self.__right_face
            case "d":
                return self.__down_face

    def get_col(self, index):
        return [row[index] for row in self.__matrix]

    def get_row(self, index):
        return self.__matrix[index][:]
    
    def set_col(self, index, col):
        for i, row in enumerate(self.__matrix):
            row[index] = col[i]
    
    def set_row(self, index, row):
        self.__matrix[index] = row[:]
