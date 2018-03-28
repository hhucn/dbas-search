Settings and structures
=======================

To add new components to D-BAS-Search it is necessary to modify the search settings.

The general structure of the setting is::

	"settings": {
            "index": {
                "analysis": {
                    "analyzer": {

			analyzer1,
			analyzer2,
			...

                    },
                    "filter": {

			filter1,
			filter2,
			...

                    }
                }
            }
        }


More details about setting up a *analyzer* or *filter* can be found in:

.. toctree::
   :maxdepth: 2

   Synonyms

The data mapping looks like::

        {
            "isPosition": start_point,
            "textversions": {
                "content": text,
                "statementUid": statement_uid
            },
            "issues": {
                "uid": uid,
                "langUid": lang_id
            }
        }

The equivalent query with *graphql* can be found in *query_with_graphql.py*.

.. warning::
	If you change the data mapping please make sure to modify the search query etc.



The general structure of the search query looks like::

    {
        "query": {
            "bool": {

                "should": [
                    {search_query1},
                    {search_query2},
                    ...
                ],
                "must": [
                    {
                        "match": {
                            "issues.uid": uid
                        }
                    },
                    {
                        "match": {
                            "isPosition": start_point
                        }
                    }
                ]
            }
        },
        highlighting_string
    }

.. warning::
    Do not delete the "must" section or you must find an other way to filter your data.

A highlighting query can look like::

	"_source": ["<field>"],
        	"highlight": {
            	"fields": {
                	"<field>": {
                    	"force_source": "true",
                    	"highlight_query": {
                        	"bool": {
                            	"should": [
                                	{search_query1},
                                	{search_query2},
                                	...
                            	]
                        }
                    }
                }
            }

Notice that *"force_source"* highlights the result with every *search_query*.

The search_queries in the search and highlight query must be the same.
