# SentinelScan Cloud MCP Server

A remote **Model Context Protocol (MCP)** server that exposes hardcoded
application security testing data (applications, scans, and issues) so that
LLM-based clients can query security posture using natural language.

This project is inspired by the HCL AppScan on Cloud MCP server, but the
server name, branding, and all responses are **hardcoded mock data** for
demonstration purposes.

## Features

The server exposes the following MCP tools:

| Tool | Description |
| --- | --- |
| `get_applications` | List all onboarded applications. |
| `get_application_details` | Get details for a single application by ID. |
| `get_scans` | List scans, optionally filtered by application. |
| `get_scan_details` | Get details for a single scan execution. |
| `get_issues` | Query issues by application, scan, severity, or status. |
| `get_issue_details` | Get full details for a specific issue (file, trace, remediation). |
| `get_dashboard_summary` | Aggregate posture summary across all apps. |

It also exposes a prompt named `sentinelscan_doc` that loads usage rules,
ID conventions, and allowed enum values into the model's context window.

## Transport

The server runs over **Streamable HTTP** on the `/mcp` endpoint, which is the
standard transport for remote MCP servers. By default it listens on
`0.0.0.0:8000`.

## Running locally

```bash
pip install -r requirements.txt
python server.py
```

The MCP endpoint will be available at:

```
http://localhost:8000/mcp
```

## Running with Docker

```bash
docker build -t sentinelscan-cloud-mcp .
docker run -p 8000:8000 sentinelscan-cloud-mcp
```

## Connecting an MCP client

Point any MCP-compatible client (Claude Desktop, Claude Code, or a custom
agent built on the Anthropic SDK) at the server URL:

```json
{
  "mcpServers": {
    "sentinelscan-cloud": {
      "url": "http://localhost:8000/mcp",
      "transport": "http"
    }
  }
}
```

## Data

All applications, scans, and issues returned by the server are hardcoded in
`server.py`. There is no external database or network call - the server
is entirely self-contained and safe to run anywhere for demos and testing.
