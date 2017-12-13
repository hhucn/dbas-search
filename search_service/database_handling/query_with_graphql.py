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


def graphql_query(query) -> dict:
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

    query = query_issue_id_by_issue_slug(issue_slug)
    response = graphql_query(query)
    return int(response.get("issue").get("uid"))


def query_issue_id_by_issue_slug(slug):
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


def query_all_users_nicknames_with_issues():
    """

    :return: all publicNames of users who took part in a discussion
    """

    return '''
           query{
                issues{
                    uid
                    users{
                        publicNickname
                    }
                }
           }
           '''


def query_all_data_by_uid(uid, is_startpoint):
    """

    :param uid: uid of the issue
    :param is_startpoint: for filtering the correct strings from db
    :return: the data requested for a suggestion
    """

    return ('''
                query{
                    statements(issueUid: %d, isStartpoint: %s){
                        isStartpoint
                        textversions{
                            content
                            authorUid
                            users{
                                publicNickname
                            }
                        }
                        issues{
                            langUid
                        }
                    }
                }
               ''') % (uid, str(is_startpoint).lower())


def query_language_of_issue_by_uid(uid):
    return ('''
               query{
                   issue(uid: %d){
                        languages{
                            uiLocales
                        }
                   }
               }
               ''') % uid


def query_all_uids():
    return ('''
            query{
                issues{
                    uid
                }
            }
            ''')


def query_every_datas_from_active_issue(uid):
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
