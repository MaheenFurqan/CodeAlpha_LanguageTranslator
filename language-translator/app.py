from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():

    try:

        data = request.json

        if not data:
            return jsonify({"error": "No data received"}), 400

        text = data.get("text")
        source = data.get("source")
        target = data.get("target")

        if not text or not source or not target:
            return jsonify({"error": "Missing translation information"}), 400

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": source + "|" + target
        }

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        result = response.json()

        translation = result["responseData"]["translatedText"]

        return jsonify({"translation": translation})


    except requests.exceptions.RequestException:

        return jsonify({
            "error": "Translation API is unavailable."
        }), 503


    except Exception:

        return jsonify({
            "error": "Something went wrong on the server."
        }), 500


app.run(debug=True)
