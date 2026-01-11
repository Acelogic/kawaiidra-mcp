# Ghidra MCP Server

A general-purpose Model Context Protocol (MCP) server for binary analysis using Ghidra's headless analyzer and decompiler.

## Features

- **Analyze any binary**: PE (Windows), ELF (Linux), Mach-O (macOS), and raw firmware
- **Decompile functions**: Get C code from compiled binaries
- **Disassembly**: View assembly listings
- **Cross-references**: Find function callers and callees
- **String analysis**: Search and list strings in binaries
- **Export results**: Save analysis to JSON for further processing
- **Multi-project support**: Organize analyses into separate Ghidra projects

## Requirements

- **Python 3.10+**
- **Ghidra 11.0+** (tested with 12.0)
- **MCP Python package**: `pip install mcp`

## Platform Support

This server works on all platforms:
- **Windows** (Windows 10+)
- **Linux** (Ubuntu, Debian, Fedora, Arch, etc.)
- **macOS** (10.15+)

## Quick Start

### 1. Install Dependencies

```bash
cd ghidra-mcp
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example configuration files and update paths for your system:

```bash
cp .env.example .env
cp .mcp.json.example .mcp.json
```

Edit `.mcp.json` and set `GHIDRA_INSTALL_DIR` to your Ghidra installation path:

**Linux/macOS:**
```json
"GHIDRA_INSTALL_DIR": "/opt/ghidra"
```

**Windows:**
```json
"GHIDRA_INSTALL_DIR": "C:\\ghidra_11.2_PUBLIC"
```

Alternatively, set the environment variable directly:

**Linux/macOS:**
```bash
export GHIDRA_INSTALL_DIR=/path/to/ghidra
```

**Windows (Command Prompt):**
```cmd
set GHIDRA_INSTALL_DIR=C:\path\to\ghidra
```

**Windows (PowerShell):**
```powershell
$env:GHIDRA_INSTALL_DIR="C:\path\to\ghidra"
```

### 3. Use with Claude Code

Open the `ghidra-mcp` folder in Claude Code. The MCP server will automatically load from `.mcp.json`.

### 4. Analyze a Binary

1. Place your binary in the `binaries/` folder, or use an absolute path
2. Use the `analyze_binary` tool to import and analyze
3. Use other tools to explore the analysis

## Available Tools

| Tool | Description |
|------|-------------|
| `analyze_binary` | Import and analyze a binary file |
| `list_analyzed_binaries` | List binaries in current project |
| `list_functions` | List all functions in a binary |
| `find_functions` | Search functions by name pattern |
| `get_function_decompile` | Decompile function to C code |
| `get_function_disassembly` | Get assembly listing |
| `get_function_xrefs` | Get cross-references to/from function |
| `search_strings` | Search strings by pattern |
| `list_strings` | List all defined strings |
| `get_binary_info` | Get binary metadata (arch, format, etc.) |
| `get_memory_map` | Get memory segments/sections |
| `export_analysis` | Export analysis to JSON file |

## Tool Examples

### Analyze a Binary

**Windows:**
```
analyze_binary
  file_path: "C:\Windows\System32\kernel32.dll"
```

**Linux:**
```
analyze_binary
  file_path: "/usr/lib/x86_64-linux-gnu/libc.so.6"
```

**macOS:**
```
analyze_binary
  file_path: "/usr/lib/libSystem.dylib"
```

### Analyze Raw Firmware

```
analyze_binary
  file_path: "firmware.bin"
  processor: "ARM:LE:32:v7"
  base_address: "0x08000000"
```

### Decompile a Function

```
get_function_decompile
  binary_name: "kernel32.dll"
  function_name: "CreateFileW"
```

### Find Crypto Functions

```
find_functions
  pattern: "crypt"
  binary_name: "target.exe"
```

### Get Cross-References

```
get_function_xrefs
  binary_name: "target.exe"
  function_name: "main"
  direction: "from"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GHIDRA_INSTALL_DIR` | Path to Ghidra installation | **Required** (no default) |
| `GHIDRA_MCP_PROJECT_DIR` | Where Ghidra projects are stored | `./projects` |
| `GHIDRA_MCP_BINARIES_DIR` | Where input binaries are stored | `./binaries` |
| `GHIDRA_MCP_EXPORTS_DIR` | Where exports are written | `./exports` |
| `GHIDRA_MCP_LOG_DIR` | Where logs are written | `./logs` |
| `GHIDRA_MCP_TIMEOUT` | Analysis timeout in seconds | `300` |
| `GHIDRA_MCP_DECOMPILE_TIMEOUT` | Decompile timeout in seconds | `180` |
| `GHIDRA_MCP_MAX_MEMORY` | JVM max memory | `4G` |

### MCP Configuration (`.mcp.json`)

**Windows:**
```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python",
      "args": ["run_server.py"],
      "env": {
        "GHIDRA_INSTALL_DIR": "C:\\ghidra_11.2_PUBLIC"
      }
    }
  }
}
```

**Linux/macOS:**
```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python",
      "args": ["run_server.py"],
      "env": {
        "GHIDRA_INSTALL_DIR": "/opt/ghidra"
      }
    }
  }
}
```

## Directory Structure

```
ghidra-mcp/
├── .mcp.json           # MCP server configuration
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── src/
│   └── ghidra_mcp/
│       ├── server.py   # MCP server implementation
│       ├── config.py   # Configuration management
│       └── scripts/    # Generated Ghidra scripts
├── projects/           # Ghidra project storage (gitignored)
├── binaries/           # Input binaries (gitignored)
├── exports/            # Exported analysis (gitignored)
└── logs/               # Runtime logs (gitignored)
```

## Supported Binary Formats

| Format | Extensions | Auto-detected |
|--------|------------|---------------|
| PE (Windows) | .exe, .dll, .sys | Yes |
| ELF (Linux) | .so, .o, (none) | Yes |
| Mach-O (macOS) | .dylib, (none) | Yes |
| Raw Binary | .bin, .fw | No (specify processor) |

## Common Processor IDs

For raw binaries, specify the processor manually:

| Architecture | Processor ID |
|--------------|--------------|
| x86 32-bit | `x86:LE:32:default` |
| x86 64-bit (AMD64) | `x86:LE:64:default` |
| ARM 32-bit | `ARM:LE:32:v7` |
| ARM 64-bit (AArch64) | `AARCH64:LE:64:default` |
| MIPS 32-bit BE | `MIPS:BE:32:default` |
| MIPS 32-bit LE | `MIPS:LE:32:default` |
| PowerPC 32-bit | `PowerPC:BE:32:default` |
| RISC-V 32-bit | `RISCV:LE:32:default` |

## Troubleshooting

### "Ghidra not found"

Ensure `GHIDRA_INSTALL_DIR` points to a valid Ghidra installation with:
- **Windows:** `support/analyzeHeadless.bat`
- **Linux/macOS:** `support/analyzeHeadless`

### "MCP SDK not installed"

```bash
pip install mcp
```

### Analysis Times Out

Increase timeout with environment variable:

**Linux/macOS:**
```bash
export GHIDRA_MCP_TIMEOUT=600
```

**Windows:**
```cmd
set GHIDRA_MCP_TIMEOUT=600
```

### Large Binary Memory Issues

Increase JVM memory:

**Linux/macOS:**
```bash
export GHIDRA_MCP_MAX_MEMORY=8G
```

**Windows:**
```cmd
set GHIDRA_MCP_MAX_MEMORY=8G
```

### Function Not Found

- Ensure the binary has been analyzed first with `analyze_binary`
- Try using the function's address instead of name (e.g., `0x401000`)
- Check if the function is in a different binary in the project

## License

MIT License
