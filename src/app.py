from flask import Flask, request, jsonify

app = Flask(__name__)

# Root route to confirm the gateway is running
@app.route("/")
def index():
    return "Moltbook MCP Gateway is running"

# MCP endpoint for agent communication
@app.route("/mcp", methods=["POST"])
def handle_mcp():
    data = request.get_json()
    print("Received MCP message:", data)
    return jsonify({"status": "ok", "received": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)