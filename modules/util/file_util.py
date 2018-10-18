__author__ = 'tinglev'

import os
from modules.util.environment import Environment

class FileUtil(object):

    @staticmethod
    def get_lines(relative_file_path):
        result = []

        if FileUtil.is_file(relative_file_path):
            with open(FileUtil.get_absolue_path(relative_file_path)) as afile:
                for line in afile:
                    result.append(line.strip())

        return result

    @staticmethod
    def get_absolue_path(relative_file_path):
        return '{}{}'.format(FileUtil.get_project_root(), relative_file_path)

    @staticmethod
    def get_project_root():
        return Environment.get_project_root().rstrip('/')

    @staticmethod
    def is_file(relative_file_path):
        return os.path.isfile(FileUtil.get_absolue_path(relative_file_path))

    @staticmethod
    def is_directory(relative_file_path):
        path = FileUtil.get_absolue_path(relative_file_path)
        return os.path.isdir(path)

    @staticmethod
    def overwite(relative_file_path, content):
        with open(FileUtil.get_absolue_path(relative_file_path), 'w+') as output_file:
            output_file.write(content)
