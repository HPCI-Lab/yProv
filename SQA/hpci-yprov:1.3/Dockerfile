FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    docker.io \
    docker-compose

# Work Directory
WORKDIR /app

# Clean and clone updated GitHub repo
RUN rm -rf /app/* && \
    git clone --branch sqa https://github.com/HPCI-Lab/yProv.git .

# Install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Make the script_dockerfile.sh script executable and run it
COPY tests.sh /app/tests.sh 
RUN chmod +x /app/tests.sh

# Default command to keep the container running
CMD ["/app/tests.sh"]