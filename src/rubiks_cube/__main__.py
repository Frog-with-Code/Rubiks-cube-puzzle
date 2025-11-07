from .utils import clear_terminal
from .cube_controller import CubeController
from .cube_factory import CubeFactory
from .cube_view import CubeView

def main():
    cube = CubeFactory().create_solved_cube()
    #cube = CubeFactory().create_cube_from_file("input.json")
    controller = CubeController(cube)
    
    cube.shuffle(1)
    clear_terminal()
    while True:
        CubeView.display_cube_state(cube)
        
        print(
            "Choose the main face. r - red, o - orange, g - green, b - blue, w - white, y - yellow"
        )
        main_face_key = input("Enter option: ")
        print("Choose the face to be rotated. l - left, u - up, r - right, d - down")
        rotated_face_key = input("Enter option: ")
        print("You wanna rotate clockwise? y - yes, n - no")
        clockwise_key = input("Enter option: ")
        
        keys = (main_face_key, rotated_face_key, clockwise_key)
        try:
            controller.rotate_cube_face(keys)
        except ValueError as error:
            print(f"{error} \nTry again\n")
            continue
        print('\n')
        
        if cube.is_solved():
            print("\nThe puzzle is solved!")
            break

if __name__ == "__main__":
    main()
