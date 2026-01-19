from flask import Flask, jsonify
from main import run_news_crew
import os

app = Flask(__name__)


@app.route("/api/run-crew", methods=["GET"])
def trigger_crew():
    # Verify a secret token to prevent strangers from running your bot
    # We will set this secret in Vercel later
    if os.getenv("CRON_SECRET") != "my-super-secret-password":
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Run the crew
        result = run_news_crew()
        return jsonify({"status": "success", "result": str(result)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
