from enum import Enum

class FaceColors(Enum):
    RED = "196"
    ORANGE = "208"
    GREEN = "46"
    BLUE = "21"
    YELLOW = "226"
    WHITE = "15"
    
    def draw_square(self):
        print(f"\033[48;5;{self.value}m   \033[0m", end=" ")
        pass