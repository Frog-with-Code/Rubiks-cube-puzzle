from enum import Enum

class FaceColors(Enum):
    RED = "48;5;196"
    ORANGE = "48;5;208"
    GREEN = "48;5;46"
    BLUE = "48;5;21"
    YELLOW = "48;5;226"
    WHITE = "48;5;15"
    
    def draw_square(self):
        print(f"\033[{self.value}m{'   '}\033[0m", end=" ")
        pass