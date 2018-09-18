Settings and structures of version 1
====================================

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
            "isPosition": is_position,
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
                            "isPosition": is_position
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

Settings and structures of version 2
====================================
Version 2 of SEARCH uses the same settings that are used in version 1.
The data-mapping is a different and can be seen in `v2/mapping`::

    {
            "mappings": {
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

This mapping can also bee seen at: https://app.swaggerhub.com/apis/TomatenMarc/SearchAPI/0.0.1
