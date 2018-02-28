"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import json
import logging

import requests

from search_service import DBAS_HOST, DBAS_PORT, DBAS_PROTOCOL


def json_to_dict(col):
    """
    Given a json object as bytes, convert it to a Python dictionary.

    :param col:
    :type col: bytes
    :rtype: dict
    """
    if isinstance(col, dict):
        return col
    elif isinstance(col, bytes):
        col = col.decode("utf-8")
    return json.loads(col)


def send_request_to_graphql(query, protocol=DBAS_PROTOCOL, host=DBAS_HOST, port=DBAS_PORT) -> dict:
    """
    Send a request to GraphQl V2 and returns response as json.

    :param port:
    :param host:
    :param protocol:
    :param query: query_string for the db request
    :return: response of the db to query
    """
    # localhost or web
    API = "{}://{}:{}/api/v2/".format(protocol, host, port)
    # API = "https://dbas.cs.uni-duesseldorf.de/api/v2/"
    url = "{}query?q={}".format(API, query)
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.error("Connection Error")
        return {}

    ret = json_to_dict(response.content)
    return ret


def pretty_print(text):
    """
    Pretty prints json.

    :param text: input to be pretty printed
    :return: pretty printed text
    """

    print(json.dumps(text, indent=2))


def get_uid_of_issue(issue_slug):
    """

    :param issue_slug: The slug of the issue
    :return: the uid of the issue
    """

    query = query_issue_id(issue_slug)
    response = send_request_to_graphql(query)
    return int(response.get("issue").get("uid"))


def query_issue_id(slug):
    """

    :param slug: the slug of the issue
    :return: the query string for finding the uid of a issue
    """

    return ("""
                query{{
                    issue(slug: "{0}"){{
                        uid
                    }}
                }}
                """).format(slug)


def query_language_of_issue(uid):
    """
    Returns the language of an issue.

    :param uid: current issue id
    :return:
    """
    return ("""
               query{{
                   issue(uid: {0}){{
                        languages{{
                            uiLocales
                        }}
                   }}
               }}
               """).format(uid)


def query_all_uid():
    return ("""
            query{
                issues{
                    uid
                }
            }
            """)


def query_data_of_issue(uid):
    return ("""
               query{{
                   statements(issueUid: {0}){{
                       isStartpoint
                       textversions{{
                            content
                            statementUid
                       }}
                       issues{{
                            uid
                            langUid
                       }}
                   }}
               }}
               """).format(uid)


def query_start_point_issue_of_statement(uid):
    return ("""
                query{{
                    statement(uid: {0}){{
                        isStartpoint
                        issues{{
                            uid
                            langUid
                        }}
                    }}
                }}
            """).format(uid)
