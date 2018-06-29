Full Text Search
================

D-BAS-Search supports a full text search.

This full text search looks up for a matching substring within a text.

A full text search query can be written like::

	"query_string": {
        	"analyzer": <analyzer>,
                "query": "*" + <search text> + "*",
                "fields": ["<field1>", "<field2>", ...]
        }

.. warning::
	Data for D-BAS-Search are stored in the <field> textversions.content.

Notice the "*" within the *query* field. 

Those "*" indicates a substring search within a text.

