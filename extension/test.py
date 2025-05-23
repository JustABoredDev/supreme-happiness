from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post-data', methods=['POST'])
def handle_post():
    data = request.get_json()  # Get JSON data from the request
    response = {
        "message": "Request received",
        "received_data": data,
        "sample_data": {"key": "value", "number": 123},
        "response": "sample response",
        "result":"hello, world!"
    }
    return jsonify(response)

app.run(debug=True)