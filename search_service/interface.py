from flask import Flask, request
import json
from search_service.elastic.search import create_connection, get_suggestions

app = Flask(__name__)


@app.route('/suggestions')
def suggest():
    id = request.args.get('id', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    start = request.args.get('start', default='false', type=str)

    if start.lower() not in ["true", "false"]:
        return "Error: Startpoint must be boolean"

    start = (start.lower() == "true")
    es = create_connection()
    res = get_suggestions(es, id, search, start)

    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
