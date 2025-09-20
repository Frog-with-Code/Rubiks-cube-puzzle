from face import Face
from colors import FaceColors

class Cube:
    def __init__(self):
        self.red_face = Face(FaceColors.RED)
        self.orange_face = Face(FaceColors.ORANGE)
        self.green_face = Face(FaceColors.GREEN)
        self.blue_face = Face(FaceColors.BLUE)
        self.white_face = Face(FaceColors.WHITE)
        self.yellow_face = Face(FaceColors.YELLOW)
        
        self.faces = []
        #self.faces.append(self.red_face, self.orange_face, self.green_face, self.blue_face,
                          #self.yellow_face, self.white_face)
        self.__sеtup_face_connections()
    
    def __sеtup_face_connections(self):
        self.red_face.set_dependency(self.green_face, self.blue_face, self.white_face, self.yellow_face)
        self.orange_face.set_dependency(self.blue_face, self.green_face, self.white_face, self.yellow_face)
        self.green_face.set_dependency(self.orange_face, self.red_face, self.white_face, self.yellow_face)
        self.blue_face.set_dependency(self.red_face, self.orange_face, self.white_face, self.yellow_face)
        self.white_face.set_dependency(self.orange_face, self.red_face, self.blue_face, self.green_face)
        self.yellow_face.set_dependency(self.red_face, self.orange_face, self.blue_face, self.green_face)
        
                            
