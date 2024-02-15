import os
import pickle
from annotation import Annotation
from contour import Contour
from status import LoginStatus


class Storage:
    """Class responsible for handling data storage."""

    @staticmethod
    def serialize(name: str, annotation: Annotation, contour_list: list[Contour]):
        """Serialize annotation and contour list to files."""
        with open("contourList_"+name, 'wb') as f:
            pickle.dump(contour_list, f)
        with open("annotation_"+name, 'wb') as f:
            pickle.dump(annotation, f)

    @staticmethod
    def deserialize(name: str) -> tuple[Annotation, list[Contour]]:
        """Deserialize annotation and contour list from files."""
        current_dir = os.getcwd()
        files_in_dir = os.listdir(current_dir)
        loaded_contour_list = []
        loaded_annotation = None

        if "contourList_" + name in files_in_dir:
            with open("contourList_" + name, 'rb') as f:
                loaded_contour_list = pickle.load(f)

        if "annotation_" + name in files_in_dir:
            with open("annotation_" + name, 'rb') as f:
                loaded_annotation = pickle.load(f)

        return loaded_annotation, loaded_contour_list

    @staticmethod
    def check_user_in_file(username: str, password: str) -> bool:
        """Check if the user exists in the user file."""
        current_dir = os.getcwd()
        files_in_dir = os.listdir(current_dir)

        if "user_manager.txt" in files_in_dir:
            with open("user_manager.txt", "r") as file:
                for line in file:
                    data = line.split()
                    if len(data) >= 4 and data[1] == username and data[2] == password:
                        user_id = int(data[0])
                        profession = data[3]
                        LoginStatus.set(user_id, LoginStatus.Profession[profession.upper()])
                        return True
        return False

    @staticmethod
    def add_user_to_file(username: str, password: str, profession: str):
        """Add a new user to the user file."""
        with open("user_manager.txt", "r") as file:
            existing_usernames = [line.split()[1] for line in file if line.strip()]

        if username in existing_usernames:
            return False  # Return False to indicate failure

        with open("user_manager.txt", "a") as file:
            user_id = len(open("user_manager.txt").readlines()) + 1  # New user id
            file.write(f"{user_id} {username} {password} {profession}\n")
            LoginStatus.set(user_id, LoginStatus.Profession[profession.upper()])
        return True  # Return True to indicate success

