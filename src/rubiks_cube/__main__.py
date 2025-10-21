from .utils import clear_terminal
from .cube_controller import CubeController


def main():
    my_cube = CubeController.create_cube_from_file("input.json")
    my_cube.shuffle(2)
    clear_terminal()
    while True:
        my_cube.display_all_faces()
        
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
            rotated_face, clockwise = CubeController.convert_keys(my_cube, keys)
        except ValueError as error:
            print(f"{error} \nTry again\n")
            continue
        print('\n')
        
        my_cube.rotate_face(rotated_face, clockwise)
        
        if my_cube.is_solved():
            print("\nThe puzzle is solved!")
            break

if __name__ == "__main__":
    main()
