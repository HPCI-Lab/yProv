FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    docker.io \
    docker-compose \
    supervisor

# Work Directory
WORKDIR /app

# Clean and clone updated GitHub repo
RUN rm -rf /app/* && \
    git clone --branch sqa https://github.com/HPCI-Lab/yProv.git .

# Install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Install additional Python dependencies
RUN pip install requests pytest

# Copy configuration files
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY docker-compose.yml /app/docker-compose.yml

# Make the script executable
RUN chmod +x /app/script_dockerfile.sh

# Keep the container running with tail
CMD ["tail", "-f", "/dev/null"]
