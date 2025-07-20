# Use a lightweight official Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system tools and dependencies
# golang because of ffuf
# perl and openssl and so on, because of nikto
RUN apt-get update && apt-get install -y \
    whatweb \
    wafw00f \
    nmap \
    golang \
    git \
    perl \
    libnet-ssleay-perl \
    openssl \
    libwhisker2-perl \
    && apt-get clean

# Set up Go path so ffuf is available
ENV PATH="/root/go/bin:${PATH}"

# Install ffuf
RUN go install github.com/ffuf/ffuf/v2@latest

# Install Nikto manually
RUN git clone https://github.com/sullo/nikto.git /opt/nikto \
    && ln -s /opt/nikto/program/nikto.pl /usr/local/bin/nikto

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY modules/ ./modules/
COPY utils/ ./utils/
COPY outputs/ ./outputs/

# Set default command
ENTRYPOINT ["python", "main.py"]
