from __future__ import annotations

import json
import sys

from .tools import build_registry


def handle(message: dict) -> dict:
    registry = build_registry()
    request_id = message.get("id")
    method = message.get("method")
    try:
        if method == "initialize":
            result = {"protocolVersion": "2025-06-18", "serverInfo": {"name": "industrial-mcp", "version": "0.1.0"}, "capabilities": {"tools": {}}}
        elif method == "tools/list":
            result = {"tools": registry.definitions()}
        elif method == "tools/call":
            params = message.get("params", {})
            output = registry.call(params["name"], params.get("arguments", {}))
            result = {"content": [{"type": "text", "text": json.dumps(output)}], "structuredContent": output}
        else:
            raise ValueError(f"unsupported method: {method}")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except (KeyError, TypeError, ValueError) as exc:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": str(exc)}}


def main() -> None:
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle(json.loads(line))), flush=True)


if __name__ == "__main__":
    main()
