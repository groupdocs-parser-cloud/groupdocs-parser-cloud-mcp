# docker build -t groupdocs/mcp-groupdocs-cloud .

# Use slim Python image
FROM python:3.12-slim-bullseye

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/

# Run server
CMD ["python", "src/server.py"]
