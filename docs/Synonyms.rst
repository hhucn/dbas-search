Synonym Search
==============

The synonym search is a part of elasiticsearch to filter and find synonyms.

Synonym search support english and german synonyms and much more languages.

D-BAS-Search supports englisch and german synonyms but can be upgraded with other languages.

The stored synonyms can be found in *search_service/analysis/*.

Notice that the synonyms should be in the coresponding text file.

Synonyms are written like::

	<synonym1, synonym2, ...>, <orginal>
	
	i.e: Coco, Rafaelo, Cococnut

To use a new synonym language for searching define a *analyzer* and a *filter* in *query_strings.py*'s settings.

To define a *analyzer* use::


	"<name of synonyms>": {
        	"tokenizer": "whitespace",
        	"filter": ["<name of synonyms>"]
	}

And to define a *filter* use::


	"<name of synonyms>": {
	        "type": "synonym",
                "synonyms_path": "<name of synonyms>.txt"
	}

Notice that *<name of synonyms>* is place holder for a new synonym file.

.. warning::

	Never miss "" at the end and the beginning of *<name of synonyms>*.

	Allways use the same *<name of synonyms>* for the *filter* and *analyzer* of each language.

	It is also important to create a new *<name of synonyms>*.txt-file in the *analysis*-folder.

You can add new *analyzer* and *filter* to the *query_strings.py*'s settings like::

	"settings": {
            "index": {
                "analysis": {
                    "analyzer": {

			analyzer1,
			analyzer2,
			....
                    },
                    "filter": {

			filter1,
			filter2,
			....
                    }
                }
            }
        }

A synonym search query looks like::

	"match_phrase": {
        	"<field>": {
                "query": <search text>,
                "analyzer": <synonym analyzer>
                }
	}

.. warning::
        Datas for D-BAS-Search are stored in the <field> textversions.content.


More information about `Synonym-Search <https://www.elastic.co/guide/en/elasticsearch/reference/5.0/analysis-synonym-tokenfilter.html>`_.
