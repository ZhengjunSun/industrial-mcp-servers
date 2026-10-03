import unittest

from industrial_mcp.server import handle
from industrial_mcp.tools import build_registry


class ServerTests(unittest.TestCase):
    def test_lists_three_tools(self):
        response = handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual(len(response["result"]["tools"]), 3)

    def test_blend_check_is_deterministic(self):
        result = build_registry().call("refinery_check_blend", {"sulfur": 1.2, "limit": 1.5})
        self.assertTrue(result["feasible"])

    def test_unknown_tool_returns_error(self):
        response = handle({"id": 2, "method": "tools/call", "params": {"name": "delete_everything"}})
        self.assertIn("error", response)


if __name__ == "__main__":
    unittest.main()
