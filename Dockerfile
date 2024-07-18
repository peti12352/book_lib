# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app/api

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/api/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app/api/

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python3", "main.py"]
