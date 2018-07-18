from core.v2.sql.db_models.author import Author
from core.v2.sql.db_models.issue import Issue
from core.v2.sql.db_models.statement import Statement


class Mapping:
    """
    This class provides data-mappings that are used for each index

    """

    @staticmethod
    def mapping() -> dict:
        """
        This is the data-mapping that is used to store the data of statement in a index.

        :return:  Mapping and data-structure of a statement
        """
        return {
            "mappings": {
                "statement": {
                    "properties": {
                        "isPosition": {
                            "type": "boolean"
                        },
                        "uid": {
                            "type": "integer"
                        },
                        "text": {
                            "type": "text"
                        },
                        "author": {
                            "properties": {
                                "uid": {
                                    "type": "integer"
                                },
                                "nickname": {
                                    "type": "text"
                                }
                            }
                        },
                        "issue": {
                            "properties": {
                                "uid": {
                                    "type": "integer"
                                },
                                "slug": {
                                    "type": "text"
                                },
                                "lang": {
                                    "type": "text"
                                },
                                "title": {
                                    "type": "text"
                                },
                                "info": {
                                    "type": "text"
                                }
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def data_mapping(statement: Statement, author: Author, issue: Issue) -> dict:
        """
        This is the json format of the statement data-structure.

        :param statement:
        :param author:
        :param issue:
        :return:
        """
        return {
            "isPosition": statement.__json__().get("uid"),
            "uid": statement.__json__().get("uid"),
            "text:": statement.__json__().get("text"),
            "author": author.__json__(),
            "issue": issue.__json__()
        }
