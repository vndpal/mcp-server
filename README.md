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

## Authentication

Modeled after HCL AppScan on Cloud's **Key ID / Key Secret** scheme, every
request to `/mcp` must include both of the following headers:

| Header | Value |
| --- | --- |
| `X-Key-Id` | `sentinel-demo-key-id-12345` |
| `X-Key-Secret` | `sentinel-demo-key-secret-abcdef67890` |

These credentials are **hardcoded** in `server.py` as the `KEY_ID` and
`KEY_SECRET` constants. There is no real authentication logic - a Starlette
middleware simply compares the incoming headers against those constants and
returns HTTP `401 Unauthorized` on mismatch.

Example check with `curl`:

```bash
curl -i https://<your-project>.vercel.app/mcp \
  -H "X-Key-Id: sentinel-demo-key-id-12345" \
  -H "X-Key-Secret: sentinel-demo-key-secret-abcdef67890"
```

Omitting or changing either header returns:

```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid credentials. Provide the 'X-Key-Id' and 'X-Key-Secret' headers on every request to the SentinelScan Cloud MCP Server."
}
```

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

## Deploying to Vercel

The repo is pre-configured to deploy as a Vercel Python serverless
function so anyone can use the server remotely over the public internet.

**Files involved:**

- `api/index.py` — Vercel entrypoint. Imports the FastMCP instance from
  `server.py` and exposes its Streamable-HTTP Starlette app as `app`,
  which Vercel's Python runtime serves automatically.
- `vercel.json` — rewrites `/mcp` (and `/mcp/*`) to `/api/index` so
  clients can use the canonical MCP path.
- `requirements.txt` — picked up by Vercel to install the `mcp` SDK.
- `server.py` — runs FastMCP in `stateless_http=True` mode, which is
  required on serverless platforms since each request is handled by a
  fresh function invocation and no session state can be preserved
  between calls.

**Deploy via the Vercel CLI:**

```bash
npm i -g vercel
vercel login
vercel           # preview deployment
vercel --prod    # production deployment
```

**Or deploy from GitHub:**

1. Push this repo to GitHub (already done on branch
   `claude/create-remote-mcp-server-PMsnL`).
2. Go to <https://vercel.com/new> and import the repository.
3. Framework preset: **Other**. Leave build/install commands empty —
   Vercel will auto-detect `requirements.txt` and the `api/` directory.
4. Click **Deploy**.

After deployment your MCP endpoint will be:

```
https://<your-project>.vercel.app/mcp
```

> **Note:** On Vercel's Hobby plan, serverless functions have a 10
> second execution timeout. That's plenty for this server since all
> responses are hardcoded, but if you later wire it up to slow
> upstream APIs you may need the Pro plan (60s) or longer.

## Connecting an MCP client

Point any MCP-compatible client (Claude Desktop, Claude Code, or a custom
agent built on the Anthropic SDK) at the server URL:

```json
{
  "mcpServers": {
    "sentinelscan-cloud": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "headers": {
        "X-Key-Id": "sentinel-demo-key-id-12345",
        "X-Key-Secret": "sentinel-demo-key-secret-abcdef67890"
      }
    }
  }
}
```

For a Vercel-hosted deployment, replace the URL:

```json
{
  "mcpServers": {
    "sentinelscan-cloud": {
      "url": "https://<your-project>.vercel.app/mcp",
      "transport": "http",
      "headers": {
        "X-Key-Id": "sentinel-demo-key-id-12345",
        "X-Key-Secret": "sentinel-demo-key-secret-abcdef67890"
      }
    }
  }
}
```

## Data

All applications, scans, and issues returned by the server are hardcoded in
`server.py`. There is no external database or network call - the server
is entirely self-contained and safe to run anywhere for demos and testing.
