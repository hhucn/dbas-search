Update Document by Query
========================
Both versions uses `update_by_query` to update a specific document of an index.
This update is done by creating a `query` which contains a `search-query` and a `update-query`.
A general `update-query` looks like::

    {
            "query": {
                <Elasticsearch-Query to find the specific document>
            },
            "script":
                <A inline-Script that contains the update information>,
                "lang": "painless"
            }
    }


Inline Syntax for a update query
================================
A inline-query should contain all information and key to update a specific document.
The keys must match those defined in the mapping of the specific index where the document
should be updated.

.. note::
    Notice: Strings must be surrounded by simple quotation marks like: `'<variable>'`. Every command must end with a
    semicolon. Booleans must be lowercase.

The inline-query syntax will then look like::

    "inline": "ctx._source.<key_1>='<a string>';" +
              "ctx._source.<key_2>= <a integer>;"

Notice that the command of `inline` is one complete string as well.