class Statement(object):
    """
    This class models the Author in the result which is then used to generate the response.

    """

    def __init__(self, content: dict = None):
        self.isPosition = content.get('is_position')
        self.uid = content.get('uid')
        self.text = content.get('content')

    def __json__(self):
        return {
            "isPosition": self.isPosition,
            "uid": self.uid,
            "text": self.text
        }
