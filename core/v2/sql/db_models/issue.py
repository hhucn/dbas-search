class Issue(object):
    """
    This class models the Issue in the result which is then used to generate the response.

    """

    def __init__(self, content: list = None):
        self.uid = content.get('issue_uid')
        self.slug = content.get('slug')
        self.lang = content.get('ui_locales')
        self.title = content.get('title')
        self.info = content.get('info')

    def __json__(self):
        return {
            "uid": self.uid,
            "slug": self.slug,
            "lang": self.lang,
            "title": self.title,
            "info": self.info
        }
