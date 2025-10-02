from .colors import FaceColors


class Face:
    edge_len = 3

    def __init__(self, color_arg):
        if isinstance(color_arg, list):
            self._matrix = color_arg[:]
        else:
            self._matrix = [[color_arg] * Face.edge_len for _ in range(Face.edge_len)]
        
    def set_dependency(self, left_face, right_face, up_face, down_face):
        self._left_face = left_face
        self._right_face = right_face
        self._up_face = up_face
        self._down_face = down_face

    def rotate(self, clockwise):
        if clockwise:
            self._matrix = [list(reversed(col)) for col in zip(*self._matrix)]
        else:
            self._matrix = [list(col) for col in zip(*self._matrix)][::-1]

    def get_face_matrix(self):
        return [row[:] for row in self._matrix]

    def get_neighbor_by_key(self, key):
        match key:
            case "l":
                return self._left_face
            case "u":
                return self._up_face
            case "r":
                return self._right_face
            case "d":
                return self._down_face

    def get_col(self, index):
        return [row[index] for row in self._matrix]

    def get_row(self, index):
        return self._matrix[index][:]
    
    def set_col(self, index, col):
        for i, row in enumerate(self._matrix):
            row[index] = col[i]
    
    def set_row(self, index, row):
        self._matrix[index] = row[:]
        
    def is_uniform(self):
        center_color = self._matrix[1][1]
        for row in self._matrix:
            for cell in row:
                if cell != center_color:
                    return False
        return True
