# Base Image
FROM python:3.9-slim

# Install dependencies
RUN pip install requests pyspark apache-airflow

# Copy application code
COPY . /app

# Set working directory
WORKDIR /app

# Set entrypoint
ENTRYPOINT ["python", "scripts/fetch_data.py"]
