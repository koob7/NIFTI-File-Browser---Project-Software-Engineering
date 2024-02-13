import os
import pickle
from annotation import ContourAnnotation, Annotation
from contour import Contour
from status import LoginStatus

class Storage:

    @staticmethod
    def serialize(name: str, annotation: Annotation, contourList: list[Contour]):
        with open("contourList_"+name, 'wb') as f:
            pickle.dump(contourList, f)
        with open("annotation_"+name, 'wb') as f:
            pickle.dump(annotation, f)

    @staticmethod
    def deserialize(name: str) -> tuple[Annotation, list[Contour]]:
        current_dir = os.getcwd()
        files_in_dir = os.listdir(current_dir)
        if "contourList_" + name in files_in_dir:
            with open("contourList_" + name, 'rb') as f:
                loaded_contour_list = pickle.load(f)

        if "annotation_" + name in files_in_dir:
            with open("annotation_" + name, 'rb') as f:
                loaded_annotation = pickle.load(f)

        return loaded_annotation, loaded_contour_list

    @staticmethod
    def check_user_in_file(username: str, password: str) -> bool:
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
        with open("user_manager.txt", "a") as file:
            user_id = len(open("user_manager.txt").readlines()) + 1  # Nowe id użytkownika
            file.write(f"{user_id} {username} {password} {profession}\n")
            LoginStatus.set(user_id, LoginStatus.Profession[profession.upper()])
        return user_id
