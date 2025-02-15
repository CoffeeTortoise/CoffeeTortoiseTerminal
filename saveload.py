import os
from constants import ENCODE, EXIT_ERR_STR, EXIT_ERR, EXIT_SUCCESS


class SaveLoad:

    @staticmethod
    def load(
            path: str,
            code: str = ENCODE
    ) -> str:
        check_path: int = SaveLoad.check_filepath(path)
        if check_path == EXIT_ERR:
            return EXIT_ERR_STR
        try:
            with open(path, 'r', encoding=code) as file:
                data: str = file.read()
            return data
        except PermissionError as e:
            print(f'Not enough rights to read {path}!\n{e}', end='\n')
            return EXIT_ERR_STR

    @staticmethod
    def save(
            path: str,
            data: str,
            code: str = ENCODE
    ) -> int:
        check_filepath: int = SaveLoad.check_filepath(path)
        if check_filepath == EXIT_ERR:
            return EXIT_ERR
        try:
            with open(path, 'w', encoding=code) as file:
                file.write(data)
            return EXIT_SUCCESS
        except PermissionError as e:
            print(f'Not enough rights to write to {path}!\n{e}', end='\n')
            return EXIT_ERR

    @staticmethod
    def check_filepath(path: str) -> int:
        if not os.path.exists(path):
            print(f'{path} doesn\'t exist!', end='\n')
            return EXIT_ERR
        elif os.path.isdir(path):
            print(f'{path} is a directory, not a file!', end='\n')
            return EXIT_ERR
        else:
            return EXIT_SUCCESS
