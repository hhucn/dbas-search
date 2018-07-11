class SQLAdapter:
    """
    This class is a adapter between sql-files and python-files.
    With a SQLAdapter it is possible to use a sql-file within a python-method.
    """

    def __init__(self, path: str):
        """
        Init a SQLAdapter with a specific path.

        :param path: Path where the sql-file is stored.
        """
        self.path = path

    def read_file(self) -> str:
        """
        Reads the sql file defined in path and returns it as a string.

        :return: sql-file as string
        """
        file = open(self.path, 'r')
        res = file.read()
        file.close()
        return res
