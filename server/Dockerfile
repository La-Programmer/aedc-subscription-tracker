# Use the official Python 3.11 image from the Alpine variant
FROM python:3.12-alpine

LABEL org.opencontainers.image.authors="name: Kelvin Johnson-Chu, email: kelvin.johnson-chu@abujaelectricity.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update \
    && apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    linux-headers

WORKDIR /srv

# Install Python dependencies
RUN pip install -r requirements.txt 

COPY . /srv

# Expose the port the app runs on
EXPOSE 8000

# Define the entrypoint command to fun the flask app
CMD ["python3", "-m", "api.v1.app"]