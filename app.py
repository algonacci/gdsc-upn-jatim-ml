import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from helpers import genai

app = Flask(__name__)

CORS(app, resources={
     r"/*": {"origins": ["http://localhost:5173", "https://gdsc-upn-jatim-fe.vercel.app"]
             }
     })


@app.route("/")
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API",
        },
        "data": None,
    }), 200


@app.route("/generate_text", methods=["GET", "POST"])
def generate_text():
    if request.method == "POST":
        input_data = request.get_json()
        prompt = input_data["prompt"]

        model = genai.GenerativeModel(
            model_name="gemini-pro",
        )

        text_result = model.generate_content(prompt)

        return jsonify({
            "status": {
                "code": 200,
                "message": "Success generate text",
            },
            "data": {
                "result": text_result.text,
            }
        }), 200
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None,
        }), 405


@app.route("/generate_text_stream", methods=["GET", "POST"])
def generate_text_stream():
    if request.method == "POST":
        input_data = request.get_json()
        prompt = input_data["prompt"]
        model = genai.GenerativeModel(model_name="gemini-pro")

        def generate_stream():
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                print(chunk.text)
                yield chunk.text + "\n"

        return Response(stream_with_context(generate_stream()), mimetype="text/plain")
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None
        }), 405


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
