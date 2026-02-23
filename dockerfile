FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TERRAFORM_VERSION=1.10.0

# Install system dependencies
RUN apk add --no-cache \
    curl \
    unzip \
    git \
    bash \
    openssh-client

# Install Terraform dynamically based on architecture
ARG TARGETARCH
RUN case "${TARGETARCH}" in \
    "amd64") TF_ARCH="amd64" ;; \
    "arm64") TF_ARCH="arm64" ;; \
    *) TF_ARCH="amd64" ;; \
    esac && \
    curl -LO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TF_ARCH}.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_${TF_ARCH}.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_${TF_ARCH}.zip

WORKDIR /app

# Copy only requirements first for better caching
COPY infra-automation/requirements.txt /app/infra-automation/

# Install Python dependencies
RUN pip install --no-cache-dir -r infra-automation/requirements.txt

# Copy the rest of the application
COPY . /app

# Ensure scripts are executable
RUN chmod +x infra-automation/src/infra_simulator.py

# Entrypoint to run the Python orchestrator
CMD ["python", "infra-automation/src/infra_simulator.py"]