class ESQuery:

    def __init__(self, field: str = "text:", text: str = "", fuzziness: int = 1):
        self.field = field
        self.text = text
        self.fuzziness = fuzziness

    def sem_query(self):
        """
        This query does a semantic search.

        :return: Semantic search query
        """
        return {
            "query": {
                "query_string": {
                    "fields": [self.field],
                    "query": "*" + self.text + "*",
                    "fuzziness": self.fuzziness
                }
            }
        }
