# Use a lightweight official Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install required system tools
RUN apt-get update && apt-get install -y \
    whatweb \
    wafw00f \
    nmap \
    && apt-get clean

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual script into the container
COPY main.py .

# Set default command to run your script
ENTRYPOINT ["python", "main.py"]
