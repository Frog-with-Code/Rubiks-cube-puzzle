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

    def rotate(self, clockwise=True):
        if clockwise:
            self.__matrix = [list(reversed(col)) for col in zip(*self.__matrix)]
        else:
            self.__matrix = [list(col) for col in zip(*self.__matrix)][::-1]

    def get_face(self):
        return [row[:] for row in self.__matrix]
    
    def get_edge(self, index):
        return list(zip(*self.__matrix))[index]

    def get_neighbor_edges(self):
        y = self.get_edge(-1)
        left_edge = self.__left_face.get_edge(-1)
        up_edge = self.__up_face.get_edge(-1)
        right_edge = self.__right_face.get_edge(0)
        down_edge = self.__down_face.get_edge(0)
        
        return left_edge, up_edge, right_edge[::-1], down_edge[::-1]
    
    def set_edge(self, index, new_edge):
        for i in range(Face.edge_len):
            self.__matrix[i][index] = new_edge[i]
    
    def set_neighbor_edges(self, rotated_edge_surface):
        left_edge, up_edge, right_edge, down_edge = rotated_edge_surface
        self.__left_face.set_edge(-1, left_edge)
        self.__up_face.set_edge(-1, up_edge)
        self.__right_face.set_edge(0, right_edge[::-1])
        self.__down_face.set_edge(0, down_edge[::-1])
