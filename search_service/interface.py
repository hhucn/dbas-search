from flask import Flask, request, jsonify

from search_service.create_database import seed_database
from search_service.elastic.listener import start_listening
from search_service.elastic.search import create_connection, get_suggestions, get_edits, get_duplicates_or_reasons, \
    get_all_statements_with_value

app = Flask(__name__)


@app.route('/suggestions')
def suggest():
    """
    This route returns suggestions to a given search word.

    :return: results for suggestions to a given search word as a list of json objects
    """
    uid = request.args.get('id', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    start = request.args.get('start', default='false', type=str)

    if start.lower() not in ["true", "false"]:
        return "Error: Startpoint must be boolean"

    start = (start.lower() == "true")
    es = create_connection()
    res = get_suggestions(es, uid, search, start)

    return jsonify(result=res)


@app.route('/edits')
def edits():
    """
    This route returns search results for edited textversions.

    :return: results for edited textversions ad a list of as a list of json objects
    """
    uid = request.args.get('id', default=1, type=int)
    statement_uid = request.args.get('statement_uid', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    es = create_connection()
    res = get_edits(es, uid, statement_uid, search)

    return jsonify(result=res)


@app.route('/duplicates_reasons')
def duplicates_reasons():
    """
    This route returns search results of textversions for duplicates or reasons.

    :return: results for duplicated or reasoned textversions as a list of json objects
    """
    uid = request.args.get('id', default=1, type=int)
    statement_uid = request.args.get('statement_uid', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    es = create_connection()
    res = get_duplicates_or_reasons(es, search, uid, statement_uid)

    return jsonify(result=res)


@app.route('/statements')
def statements_with_value():
    """
    This route returns search results for textversions of statements matching a given value.

    :return: results for textversions of statements matching a given value
    """
    uid = request.args.get('id', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    es = create_connection()
    res = get_all_statements_with_value(es, search, uid)

    return jsonify(result=res)


@app.route('/init', methods=['POST'])
def init():
    """
    This route seeds the elastic search index and starts the insertion-listener for the DBAS database.
    This route takes the arguments DBAS_PROTOCOL, DBAS_HOST, DBAS_PORT.

    :return: list of json-objects of the delivered arguments
    """
    app.logger.info("foo")
    results = request.get_json(force=True)

    protocol = results["DBAS_PROTOCOL"]
    host = results["DBAS_HOST"]
    port = results["DBAS_PORT"]

    seed_database(protocol, host, port)
    start_listening()

    return jsonify(result=results)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
