from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "AI News Bot is Active! 🚀 (Running via GitHub Actions)"


@app.route("/api/run-crew", methods=["GET"])
def trigger_crew():
    return jsonify(
        {
            "status": "active",
            "message": "The AI Bot logic is running on GitHub Actions schedule (Every 6 Hours) to bypass Vercel serverless limits.",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
