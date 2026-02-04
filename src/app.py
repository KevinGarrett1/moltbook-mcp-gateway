from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "ok"

@app.route("/mcp", methods=["POST"])
def mcp():
    data = request.get_json(force=True)
    print("MCP:", data)

    method = data.get("method")
    req_id = data.get("id")

    # ---- REQUIRED BY AGENT BUILDER ----
    if method == "list_tools":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "validate_threat",
                        "description": "Validate an incident",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "incident": {
                                    "type": "object"
                                }
                            },
                            "required": ["incident"]
                        }
                    }
                ]
            }
        })

    if method == "call_tool":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "verdict": "unknown",
                "confidence": 0.0
            }
        })

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
