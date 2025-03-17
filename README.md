# DevHub CMS MCP

A Model Context Protocol (MCP) integration for managing content in the DevHub CMS system.

## Installation

You will need the [uv](https://github.com/astral-sh/uv) package manager installed on your local system.

### Manual configuration of Claude Desktop

To use this server with the Claude Desktop app, add the following configuration to the "mcpServers" section of your `claude_desktop_config.json`:

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