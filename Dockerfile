# Use official Node 20 slim image, then install Python
FROM node:20-slim

# Install Python 3.12 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything in
COPY . .

# Create & activate Python venv, install Python deps
RUN python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Node dependencies (production only)
RUN npm ci --omit=dev

# Default command: activate venv & run the bot
CMD [ "sh", "-c", ". .venv/bin/activate && npm run bot -- --symbol=${SYMBOL:-SOFI} --interval=${INTERVAL:-m30}" ]
