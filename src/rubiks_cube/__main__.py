from cube import Cube
from colors import FaceColors


def main():
    cube1 = Cube()
    Cube.clear_terminal()
    while True:
        cube1.display_all_faces()
        print(
            "Choose the main face. r - red, o - orange, g - green, b - blue, w - white, y - yellow"
        )
        main_face_key = input("Enter option: ")
        print("Choose the face to be rotated. l - left, u - up, r - right, d - down")
        rotated_face_key = input("Enter option: ")
        print("You wanna rotate clockwise? y - yes, n - no")
        clockwise_key = input("Enter option: ")
        keys = (main_face_key, rotated_face_key, clockwise_key)
        #Cube.clear_terminal()
        
        try:
            cube1.rotate_face(keys)
        except ValueError as error:
            print(f"{error} \nTry again\n")
            continue
        
        if cube1.is_solved():
            print("\nThe puzzle is solved!")
            break

if __name__ == "__main__":
    main()
