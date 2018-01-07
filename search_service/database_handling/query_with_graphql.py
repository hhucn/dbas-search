"""
.. codeauthor:: Marc Feger <marc.feger@uni-duesseldorf.de>
"""
import json

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


def send_request_to_graphql(query) -> dict:
    """

    :param query: query_string for the db request
    :return: response of the db to query
    """
    # localhost or web
    API = "{}://{}:{}/api/v2/".format(DBAS_PROTOCOL, DBAS_HOST, DBAS_PORT)
    # API = "https://dbas.cs.uni-duesseldorf.de/api/v2/"
    url = "{}query?q={}".format(API, query)

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return {}

    # assert_is_not_none(response)
    ret = json_to_dict(response.content)
    # assert_is_not_none(ret)
    return ret


def pretty_print(text):
    """

    :param text: input to be pretty printed
    :return: pretty printed text
    """

    print(json.dumps(text, indent=2))


def get_length_of_json(json_data):
    """

    :param json_data:
    :return: the length of a json object
    """

    return len(json_data)


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

    return ('''
                query{
                    issue(slug: "%s"){
                        uid
                    }
                }
                ''') % slug


def query_language_of_issue(uid):
    return ('''
               query{
                   issue(uid: %d){
                        languages{
                            uiLocales
                        }
                   }
               }
               ''') % uid


def query_all_uid():
    return ('''
            query{
                issues{
                    uid
                }
            }
            ''')


def query_data_of_issue(uid):
    return ('''
               query{
                   statements(issueUid: %d){
                       isStartpoint
                       textversions{
                            content
                       }
                       issues{
                            uid
                            langUid
                       }
                   }
               }
               ''') % int(uid)
