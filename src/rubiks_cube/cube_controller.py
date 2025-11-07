from .cube import Cube
from .face import Face
from .validator import Validator


class CubeController:
    """
    Manages creation and manipulation of Cube objects through high-level operations.

    This includes generating a solved cube, loading cube state from JSON files,
    and parsing user key commands into cube face rotations.
    """

    def __init__(self, cube: Cube) -> None:
        self.cube = cube

    def _convert_keys(self, keys: tuple[str, str, str]) -> tuple[Face, bool]:
        """
        Parse a triple of user keys into a face rotation command.

        Args:
            keys: Tuple of three strings: (observed_face, neighbor_face, clockwise_flag).
                  Face keys: 'r','o','g','b','w','y'. Clockwise flag: 'y' for clockwise.

        Returns:
            A tuple containing:
                - The Face object to rotate.
                - A boolean indicating rotation direction (True=clockwise).

        Raises:
            ValidatorError: If keys are invalid or not recognized.
        """
        formatted_keys = tuple(key.strip().lower() for key in keys)
        Validator.validate_keys(formatted_keys)

        observed_face_key, rotated_face_key, clockwise_key = formatted_keys
        observed_face = self.cube._get_face_by_key(observed_face_key)
        rotated_face = observed_face.get_neighbor_by_key(rotated_face_key)
        clockwise = clockwise_key == "y"

        return rotated_face, clockwise

    def rotate_cube_face(self, keys: tuple[str, str, str]) -> None:
        """Rotate a face of the Rubik's cube.

        Converts user input (key combination) into a rotation command for a specific
        face and delegates the operation to the Cube object.

        Args:
            keys (tuple[str, str, str]): A tuple of three keys that determines
                which face to rotate and the rotation direction (clockwise or
                counterclockwise).
        """
        rotated_face, clockwise = self._convert_keys(keys)
        self.cube.rotate_face(rotated_face, clockwise)
