#!flask/bin/python
from collections import defaultdict
from datetime import datetime, timedelta
import operator

from flask import Flask, jsonify, request, make_response, abort

from sumple_api.metric_item import MetricItems, MetricItem


app = Flask(__name__)
DATA = defaultdict(MetricItems)


@app.errorhandler(400)
def bad_request(err):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({"error": "Nothing to see here"}), 404)


@app.route("/metric/<key>", methods=["POST"])
def post_value_for_key(key):
    """Read the body for a `value` object within it. If a `value` object isn't
    in the json post body, then throw a 400 error. Cast `value` as an `int`
    object. If that fails, then throw a 400 error.
    """
    data_keys = request.json.keys()
    post_date = datetime.now()
    if "value" not in data_keys:
        abort(400, "POST body must contains a `value` object.")
    try:
        value = int(request.json["value"])
    except:
        abort(400, "POST body value must be an integer.")
    metric_item = MetricItem(date=post_date, value=value)
    DATA[key].append(metric_item)
    DATA[key].data.sort(key=operator.attrgetter("date"))
    return jsonify(request.json)


@app.route("/metric/<key>/sum", methods=["GET"])
def get_sum_for_key(key):
    """Retrieve the sum of n number of values that have been posted within one
    hour from call time.
    """
    get_date = request.date if request.date else datetime.now()
    if key not in DATA.keys():
        abort(400, "Key does not exist.")
    metric_items = DATA[key]
    filter_time = get_date - timedelta(hours=1)
    metric_items.purge(filter_time)
    summation = sum(map(operator.attrgetter("value"), metric_items.data))
    return jsonify({"value": summation})


if __name__ == "__main__":
    app.run(debug=True)
