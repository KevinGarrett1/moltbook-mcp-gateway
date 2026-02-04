from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "MCP server is running"


@app.route("/mcp", methods=["POST"])
def mcp():
    data = request.get_json(force=True)
    print("MCP request:", data)

    method = data.get("method")
    req_id = data.get("id")

    # -----------------------------
    # REQUIRED: list_tools
    # -----------------------------
    if method == "list_tools":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "validate_threat",
                        "description": "Validate an incident and return a threat assessment",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "incident": {
                                    "type": "object",
                                    "description": "Incident payload"
                                }
                            },
                            "required": ["incident"]
                        }
                    }
                ]
            }
        })

    # -----------------------------
    # REQUIRED: call_tool
    # -----------------------------
    if method == "call_tool":
        params = data.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name != "validate_threat":
            return jsonify({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            })

        incident = arguments.get("incident", {})

        # Deterministic placeholder response
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "verdict": "unknown",
                "confidence": 0.0,
                "requires_human": True
            }
        })

    # -----------------------------
    # Fallback
    # -----------------------------
    return jsonify({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32600,
            "message": "Invalid request"
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
