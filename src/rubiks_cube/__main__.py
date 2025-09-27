from cube import Cube
from colors import FaceColors


def main():
    cube1 = Cube()
    flag = True
    while flag:
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
        cube1.rotate_face(keys)

if __name__ == "__main__":
    main()
