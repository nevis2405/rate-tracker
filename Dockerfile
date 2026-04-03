# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY backend/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]