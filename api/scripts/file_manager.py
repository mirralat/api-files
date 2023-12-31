import os
import subprocess
from abc import ABC, abstractmethod
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from dotenv import load_dotenv

load_dotenv()


class FileManagerTemplate(ABC):
    @abstractmethod
    def __init__(self, pwd):
        self.pwd = pwd

    @abstractmethod
    def get_all_user_files(self, user):
        pass

    @abstractmethod
    def upload_user_file(self, user, file):
        pass

    @abstractmethod
    def delete_user_file(self, user, file):
        pass

    @abstractmethod
    def rename_user_file(self, user, file, new_file):
        pass


class FileManager(FileManagerTemplate):
    def __init__(self, pwd):
        FileManagerTemplate.__init__(self, pwd)

    def get_all_user_files(self, user) -> List:
        try:
            user_files = os.listdir(f'{self.pwd}/{user}')
        except FileNotFoundError:
            return []
        return user_files

    def upload_user_file(self, user, file) -> bool:
        try:
            users = os.listdir(self.pwd)
            user_in_dir = False
            for us in users:
                if us == str(user):
                    user_in_dir = True
                    break
            if not user_in_dir:
                subprocess.run(['mkdir', f'{self.pwd}\\{str(user)}'], shell=True)
            with open(os.path.join(f'{self.pwd}/{user}', file.filename), 'wb') as f:
                shutil.copyfileobj(file.file, f)
        except Exception:
            return False
        return True

    def delete_user_file(self, user, file) -> bool:
        try:
            os.remove(f'{self.pwd}/{user}/{file}')
        except FileNotFoundError:
            return False
        return True

    def rename_user_file(self, user, file, new_file) -> bool:
        try:
            os.rename(f'{self.pwd}/{user}/{file}', f'{self.pwd}/{user}/{new_file}')
        except FileNotFoundError:
            return False
        return True

