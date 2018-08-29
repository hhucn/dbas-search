class Author(object):
    """
    This class models the Author in the result which is then used to generate the response.

    """

    def __init__(self, content: dict = None):
        self.uid = content.get('author_uid')
        self.nickname = content.get('public_nickname')

    def __json__(self):
        return {
            "uid": self.uid,
            "nickname": self.nickname
        }
