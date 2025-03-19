# DevHub CMS MCP

[![smithery badge](https://smithery.ai/badge/@devhub/devhub-cms-mcp)](https://smithery.ai/server/@devhub/devhub-cms-mcp)

A Model Context Protocol (MCP) integration for managing content in the [DevHub CMS system](https://www.devhub.com/).

## Installation

You will need the [uv](https://github.com/astral-sh/uv) package manager installed on your local system.

### Installing via Smithery

To install DevHub CMS MCP for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@devhub/devhub-cms-mcp):

```bash
npx -y @smithery/cli install @devhub/devhub-cms-mcp --client claude
```

### Manual configuration of Claude Desktop

To use this server with the [Claude Desktop app](https://claude.ai/download), add the following configuration to the "mcpServers" section of your `claude_desktop_config.json`:

```
{
    "mcpServers": {
        "devhub_cms_mcp": {
            "command": "uvx",
            "args": [
                "devhub-cms-mcp"
            ],
            "env": {
                "DEVHUB_API_KEY": "YOUR_KEY_HERE",
                "DEVHUB_API_SECRET": "YOUR_SECRET_HERE",
                "DEVHUB_BASE_URL": "https://yourbrand.cloudfrontend.net"
            }
        }
    }
}
```

After updating the config, restart Claude Desktop.

## Manual configuration for Cursor

This MCP can also be used in cursor with a similar configuration from above added to your [Cursor](https://www.cursor.com/) global environment or to individual projects.

Examples [here](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)

## Local development

### Clone the repo (or your fork)

```
git clone git@github.com:devhub/devhub-cms-mcp.git
```

### Manual configuration of Claude Desktop

To use this server with the Claude Desktop app for local development, add the following configuration to the "mcpServers" section of your `claude_desktop_config.json`:

```
{
    "mcpServers": {
        "devhub_cms_mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "/YOUR/LOCAL/PATH/devhub-cms-mcp/",
                "run",
                "main.py"
            ],
            "env": {
                "DEVHUB_API_KEY": "YOUR_KEY_HERE",
                "DEVHUB_API_SECRET": "YOUR_SECRET_HERE",
                "DEVHUB_BASE_URL": "https://yourbrand.cloudfrontend.net"
            }
        }
    }
}
```

After updating the config, restart Claude Desktop.

### Configuration for running with `uv` directly

This MCP requires the following environment variables to be set:

```bash
export DEVHUB_API_KEY="your_api_key"
export DEVHUB_API_SECRET="your_api_secret"
export DEVHUB_BASE_URL="https://yourbrand.cloudfrontend.net"
```

Then run the MCP

```
uv run main.py
```

## Available Tools

This MCP provides the following tools for interacting with DevHub CMS:

### Location Management

- **get_hours_of_operation(location_id)**: Gets the hours of operation for a specific DevHub location. Returns a structured list of time ranges for each day of the week.
- **update_hours(location_id, new_hours, hours_type='primary')**: Updates the hours of operation for a DevHub location.
- **get_nearest_location(business_id, latitude, longitude)**: Finds the nearest DevHub location based on geographic coordinates.

### Content Management

- **get_blog_post(post_id)**: Retrieves a single blog post by ID, including its title, date, and HTML content.
- **create_blog_post(site_id, title, content)**: Creates a new blog post. The content should be in HTML format and should not include an H1 tag.
- **update_blog_post(post_id, title=None, content=None)**: Updates an existing blog post's title and/or content.

### Media Management

- **upload_image(base64_image_content, filename)**: Uploads an image to the DevHub media gallery. Supports webp, jpeg, and png formats. The image must be provided as a base64-encoded string.

## Usage with LLMs

This MCP is designed to be used with Large Language Models that support the Model Context Protocol. It allows LLMs to manage content in DevHub CMS without needing direct API access integrated into the LLM natively.

## Testing

This package includes a test suite with mocked requests to the DevHub API, allowing you to test the functionality without making actual API calls.

### Running Tests

To run the tests, first install the package with test dependencies:

```bash
uv pip install -e ".[test]"
```

Run the tests with pytest:

```bash
pytest
```

For more detailed output and test coverage information:

```bash
pytest -v --cov=devhub_cms_mcp
```

### Test Structure

- `tests/devhub_cms_mcp/test_mcp_integration.py`: Tests for MCP integration endpoints
