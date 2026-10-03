from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    schema: dict
    function: Callable[[dict], dict]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def definitions(self) -> list[dict]:
        return [{"name": t.name, "description": t.description, "inputSchema": t.schema} for t in self._tools.values()]

    def call(self, name: str, arguments: dict) -> dict:
        if name not in self._tools:
            raise KeyError(name)
        return self._tools[name].function(arguments)


EVENTS = [
    {"id": "evt-1", "severity": "warning", "message": "synthetic link flap"},
    {"id": "evt-2", "severity": "critical", "message": "synthetic registration reject"},
]

PROVISIONS = {
    "demo-8": "Fictional provision 8: automated research outputs require human verification.",
}


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(Tool(
        "telecom_search_events", "Search synthetic telecom events",
        {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["query"]},
        lambda args: {"events": [e for e in EVENTS if args["query"].lower() in e["message"].lower()][:min(int(args.get("limit", 10)), 50)]},
    ))

    def check_blend(args: dict) -> dict:
        sulfur = float(args["sulfur"])
        limit = float(args.get("limit", 1.5))
        return {"feasible": sulfur <= limit, "sulfur": sulfur, "limit": limit, "synthetic": True}

    registry.register(Tool(
        "refinery_check_blend", "Check a hypothetical sulfur constraint",
        {"type": "object", "properties": {"sulfur": {"type": "number"}, "limit": {"type": "number"}}, "required": ["sulfur"]},
        check_blend,
    ))
    registry.register(Tool(
        "legal_lookup_provision", "Retrieve a fictional provision by identifier",
        {"type": "object", "properties": {"provision_id": {"type": "string"}}, "required": ["provision_id"]},
        lambda args: {"provision_id": args["provision_id"], "text": PROVISIONS.get(args["provision_id"]), "requires_review": True},
    ))
    return registry
