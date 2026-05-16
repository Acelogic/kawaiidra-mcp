"""Tests for the run_server.py startup wrapper."""

import builtins
import runpy
import types
from pathlib import Path


RUN_SERVER_PATH = Path(__file__).parent.parent / "run_server.py"


def _fake_server_module() -> types.ModuleType:
    module = types.ModuleType("kawaiidra_mcp.server")

    async def main():
        return None

    module.main = main
    return module


def test_preloads_jpype_before_importing_mcp_server(monkeypatch):
    """JPype should import before the MCP server module starts its stdio loop."""
    monkeypatch.delenv("KAWAIIDRA_USE_BRIDGE", raising=False)
    imports: list[str] = []
    original_import = builtins.__import__

    def tracking_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "jpype":
            imports.append("jpype")
            return types.ModuleType("jpype")
        if name == "kawaiidra_mcp.server":
            imports.append("kawaiidra_mcp.server")
            return _fake_server_module()
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", tracking_import)

    runpy.run_path(str(RUN_SERVER_PATH), run_name="__run_server_test__")

    assert imports == ["jpype", "kawaiidra_mcp.server"]


def test_missing_jpype_does_not_stop_server_import(monkeypatch):
    """The wrapper should still start in subprocess mode when JPype is absent."""
    monkeypatch.delenv("KAWAIIDRA_USE_BRIDGE", raising=False)
    imports: list[str] = []
    original_import = builtins.__import__

    def tracking_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "jpype":
            imports.append("jpype")
            raise ImportError("No module named 'jpype'")
        if name == "kawaiidra_mcp.server":
            imports.append("kawaiidra_mcp.server")
            return _fake_server_module()
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", tracking_import)

    runpy.run_path(str(RUN_SERVER_PATH), run_name="__run_server_test__")

    assert imports == ["jpype", "kawaiidra_mcp.server"]


def test_bridge_disabled_skips_jpype_import(monkeypatch):
    """Subprocess mode should not require JPype just to start the server."""
    imports: list[str] = []
    original_import = builtins.__import__

    def tracking_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "jpype":
            imports.append("jpype")
            raise AssertionError("JPype should not be imported when bridge mode is disabled")
        if name == "kawaiidra_mcp.server":
            imports.append("kawaiidra_mcp.server")
            return _fake_server_module()
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setenv("KAWAIIDRA_USE_BRIDGE", "false")
    monkeypatch.setattr(builtins, "__import__", tracking_import)

    runpy.run_path(str(RUN_SERVER_PATH), run_name="__run_server_test__")

    assert imports == ["kawaiidra_mcp.server"]
