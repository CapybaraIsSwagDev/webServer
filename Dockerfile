# 1. Use an existing base image (e.g., Python)
FROM python:3.14.3-slim
# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies first (better for Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
# -w 4: 4 worker processes
# -b 0.0.0.0:8000: Bind to all interfaces on port 8000
# app:app: Look for a file named 'app.py' with a Flask instance named 'app'
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]