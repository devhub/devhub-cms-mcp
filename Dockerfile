# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
FROM python:3.10-alpine

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy project files
COPY pyproject.toml ./
COPY main.py ./
COPY src/ ./src/
COPY README.md ./
COPY uv.lock ./
COPY tests/ ./tests/

# Install pip and project dependencies
RUN pip install --upgrade pip \
    && pip install .

# Expose port if necessary (not required for stdio transport)

# Default command to run the MCP server
CMD ["python", "main.py"]
