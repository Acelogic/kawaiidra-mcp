# Cross-Platform Support

This Ghidra MCP server now supports all major platforms without any hardcoded paths.

## Changes Made

### 1. Removed Hardcoded Paths
- **config.py**: Removed hardcoded Windows path `C:\Users\Meow\Documents\Projects\ghidra_12.0_PUBLIC`
- **config.py**: Made `GHIDRA_INSTALL_DIR` environment variable required (no default fallback)
- **.mcp.json**: Removed user-specific paths, now uses placeholder `/path/to/ghidra`

### 2. Added Configuration Examples
- **.env.example**: Template for environment variable configuration
- **.mcp.json.example**: Template for MCP server configuration
- Both files include platform-specific examples for Windows, Linux, and macOS

### 3. Updated Documentation
- **README.md**: Added comprehensive cross-platform examples
- **README.md**: Added "Platform Support" section
- **README.md**: Updated all command examples to show Windows, Linux, and macOS variants
- **README.md**: Updated troubleshooting section with platform-specific guidance

## Platform-Specific Behaviors

The codebase includes platform-specific handling that is **necessary** for proper operation:

### Windows-Specific Code (Intentional)
1. **run_server.py (lines 7-9)**: Sets `WindowsProactorEventLoopPolicy` for proper async subprocess handling on Windows
2. **server.py (lines 45-59)**: `_quote_windows_arg()` function for cmd.exe argument escaping
3. **server.py (lines 79-96)**: Special handling for `.bat` files on Windows with shell=True
4. **config.py (lines 59-60)**: Checks for both `analyzeHeadless.bat` (Windows) and `analyzeHeadless` (Unix)

These platform-specific code paths are **correct** and **necessary** for cross-platform support. They:
- Only activate on their respective platforms
- Don't prevent the code from running on other platforms
- Handle platform-specific requirements (e.g., cmd.exe quoting, Windows event loops)

## How to Configure for Each Platform

### Linux
```bash
export GHIDRA_INSTALL_DIR=/opt/ghidra
# or /home/user/ghidra_11.2_PUBLIC
```

### macOS
```bash
export GHIDRA_INSTALL_DIR=/Applications/ghidra_11.2_PUBLIC
# or /opt/ghidra
```

### Windows (Command Prompt)
```cmd
set GHIDRA_INSTALL_DIR=C:\ghidra_11.2_PUBLIC
```

### Windows (PowerShell)
```powershell
$env:GHIDRA_INSTALL_DIR="C:\ghidra_11.2_PUBLIC"
```

## Verification

To verify the server works on your platform:

1. Set `GHIDRA_INSTALL_DIR` environment variable
2. Update `.mcp.json` with your Ghidra path
3. Run `python run_server.py` to test
4. The server should start without errors if Ghidra is found

## Error Handling

If `GHIDRA_INSTALL_DIR` is not set, the server will now:
1. Raise a clear error message
2. Show example paths for all platforms
3. Prevent startup rather than using an invalid default

This ensures users are aware they need to configure their environment before use.
