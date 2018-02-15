from flask import Flask, request
import json
from search_service.elastic.search import create_connection, get_suggestions, get_edits, get_duplicates_or_reasons

app = Flask(__name__)


@app.route('/suggestions')
def suggest():
    uid = request.args.get('id', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    start = request.args.get('start', default='false', type=str)

    if start.lower() not in ["true", "false"]:
        return "Error: Startpoint must be boolean"

    start = (start.lower() == "true")
    es = create_connection()
    res = get_suggestions(es, uid, search, start)

    return json.dumps(res)


@app.route('/edits')
def edits():
    uid = request.args.get('id', default=1, type=int)
    statement_uid = request.args.get('statement_uid', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    es = create_connection()
    res = get_edits(es, uid, statement_uid, search)

    return json.dumps(res)


@app.route('/duplicates_reasons')
def duplicates_reasons():
    uid = request.args.get('id', default=1, type=int)
    statement_uid = request.args.get('statement_uid', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    es = create_connection()
    res = get_duplicates_or_reasons(es, search, uid, statement_uid)

    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
