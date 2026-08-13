# Weather MCP Server

A simple [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that
gives Claude (or any MCP-compatible client) a live tool for checking current weather
conditions, backed by the [OpenWeatherMap](https://openweathermap.org/api) API.

Built as a hands-on project to learn MCP server development — the pattern used here
(wrapping a REST API as a typed, LLM-callable tool) is the same one used to build
agent tooling for internal business systems (CRM, ERP, ticketing, etc.).

## What it does

Exposes one tool, `get_current_weather`, that takes a city name and returns the
current conditions — description, temperature, "feels like," and humidity — by
calling the OpenWeatherMap Current Weather API in real time.

**Example:**
> "What's the weather in Tokyo right now?"
> → *Weather in Tokyo: light rain, 78°F (feels like 81°F), 70% humidity*

## Tech stack

- Python 3.10+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (v1.x, `mcp[cli]`)
- `httpx` for async HTTP calls
- `python-dotenv` for local secrets management
- Transport: stdio (runs as a local subprocess of the MCP client)

## Setup

1. **Get an API key** — sign up free at [openweathermap.org/api](https://openweathermap.org/api)
   and copy your key from the API keys tab. New keys can take up to ~2 hours to activate.

2. **Clone and install:**
   ```bash
   git clone <your-repo-url>
   cd weather-mcp-server
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\Activate.ps1
   pip install "mcp[cli]<2" httpx python-dotenv
   ```

3. **Add your API key** — create a `.env` file in the project root:
   ```
   OWM_API_KEY=your_key_here
   ```

4. **Test it standalone** with the MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector python server.py
   ```
   Open the Tools tab, run `get_current_weather` with a city name, and confirm you
   get a live result back.

## Connecting to a client

**Claude Desktop** — add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "weather": {
      "command": "/absolute/path/to/weather-mcp-server/venv/bin/python",
      "args": ["/absolute/path/to/weather-mcp-server/server.py"]
    }
  }
}
```
Restart Claude Desktop after editing the config.

**Claude Code:**
```bash
claude mcp add weather -- /absolute/path/to/venv/bin/python /absolute/path/to/server.py
```
Fully restart the Claude Code app/CLI process afterward — MCP tool lists are loaded
once at startup, so a new server won't appear in an existing session.

## Project structure

```
weather-mcp-server/
├── server.py        # MCP server + get_current_weather tool
├── .env              # API key (not committed)
├── .gitignore
└── README.md
```

## Notes / lessons learned

- The MCP Python SDK shipped a major v2 rework in mid-2026 that restructured how
  `FastMCP` is imported; this project pins `mcp[cli]<2` to stay on the stable v1.x API
  used throughout this code.
- MCP clients read their server/tool list once at process startup — registering a new
  server requires a full app/CLI restart, not just a new chat session.

## Possible next steps

- Add a `get_forecast` tool (5-day forecast endpoint)
- Add input validation / friendlier error messages for ambiguous city names
- Package with `uv` for faster, more reproducible installs
- Deploy as a remote (HTTP/SSE) server instead of local stdio
