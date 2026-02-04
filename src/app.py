from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Moltbook MCP Gateway is running"


@app.route("/mcp", methods=["POST"])
def handle_mcp():
    data = request.get_json(force=True)
    print("Received MCP message:", data)

    # -----------------------------
    # MCP INITIALIZE (HANDSHAKE)
    # -----------------------------
    if data.get("method") == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": data.get("id"),
            "result": {
                "serverInfo": {
                    "name": "moltbook-mcp-gateway",
                    "version": "0.1.0"
                },
                "capabilities": {
                    "tools": [
                        {
                            "name": "validate_threat",
                            "description": "Validate an incident and return a structured threat assessment",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "incident": {
                                        "type": "object",
                                        "description": "Incident payload from Moltbook"
                                    }
                                },
                                "required": ["incident"]
                            }
                        }
                    ]
                }
            }
        }), 200

    # -----------------------------
    # MCP TOOL INVOCATION
    # -----------------------------
    if data.get("method") == "tools/call":
        tool_name = data["params"]["name"]
        arguments = data["params"].get("arguments", {})

        if tool_name == "validate_threat":
            result = {
                "verdict": "unknown",
                "confidence": 0.0,
                "requires_human": True,
                "status": "acknowledged"
            }

            return jsonify({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": result
            }), 200

        return jsonify({
            "jsonrpc": "2.0",
            "id": data.get("id"),
            "error": {
                "code": -32601,
                "message": f"Tool not found: {tool_name}"
            }
        }), 404

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return jsonify({
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "error": {
            "code": -32600,
            "message": "Invalid MCP request"
        }
    }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
