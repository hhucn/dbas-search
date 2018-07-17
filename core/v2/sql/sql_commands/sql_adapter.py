import os


class SQLAdapter:
    """
    This class is a adapter between sql-files and python-files.
    With a SQLAdapter it is possible to use a sql-file within a python-method.
    """

    def __init__(self, file: str):
        """
        Init a SQLAdapter with a specific path.

        :param file: The file-name where the sql that should be used is stored
        """
        self.file = file

    @staticmethod
    def __get_cmd_folder() -> str:
        """
        The sql commands are stored in the commands-folder.
        This folder must be at the same place the SQLAdapter is stored.

        :return: name of the folder where the sql files are stored.
        """
        return os.path.dirname(os.path.abspath(__file__)) + '/commands'

    def read_file(self) -> str:
        """
        Reads the sql file defined in path and returns it as a string.

        :return: sql-file as string
        """
        with open(self.__get_cmd_folder() + '/' + self.file, 'r') as file:
            res = file.read()
        return res
