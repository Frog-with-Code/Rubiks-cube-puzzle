from colors import FaceColors

class Face:
    def __init__(self, color):
        self.__matrix = [[color] * 3 for _ in range(3)]
        
    def set_dependency(self, left_face, right_face, up_face, down_face):
        self.left_face = left_face
        self.right_face = right_face
        self.up_face = up_face
        self.down_face = down_face
        
    def rotate_face(self, clockwise=True):
        if clockwise:
            self.__matrix = [list(reversed(col)) for col in zip(*self.__matrix)]
        else:
            self.__matrix = [list(col) for col in zip(*self.__matrix)][::-1]
            
    def display_face(self):
        for row in self.__matrix:
            for cell in row:
                pass