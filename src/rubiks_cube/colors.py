from enum import Enum

class FaceColors(Enum):
    """
    Enumeration of standard Rubik's Cube face colors with ANSI 256-color codes.

    Members:
        RED: ANSI code "196" for red background.
        ORANGE: ANSI code "208" for orange background.
        GREEN: ANSI code "46" for green background.
        BLUE: ANSI code "21" for blue background.
        YELLOW: ANSI code "226" for yellow background.
        WHITE: ANSI code "15" for white background.
    """
    RED = "196"
    ORANGE = "208"
    GREEN = "46"
    BLUE = "21"
    YELLOW = "226"
    WHITE = "15"
    
    def draw_square(self):
        """
        Render a single colored square in the terminal using ANSI escape codes.
        """
        print(f"\033[48;5;{self.value}m   \033[0m", end=" ")
        pass