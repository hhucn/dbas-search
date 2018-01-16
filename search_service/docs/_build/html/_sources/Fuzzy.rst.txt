Fuzzy Search
============

D-BAS-Search supports a fuzzy search.

The fuzzy search query can be found in  *query_string.py*.

A query string for fuzzy search looks like::

	"match": {
        	"<field>": {
                	"query": <search text>,
                        "fuzziness": <fuzziness>,
                        "prefix_length": <leading characters not fuzzified>
		}
	}

.. warning::
	Datas for D-BAS-Search are stored in the <field> textversions.content.


