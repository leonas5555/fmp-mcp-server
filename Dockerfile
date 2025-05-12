# Use python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make the server executable
RUN chmod +x fmp_mcp_server.py

# Expose the port
EXPOSE 8080

# Set the entrypoint
CMD ["python", "fmp_mcp_server.py"]
