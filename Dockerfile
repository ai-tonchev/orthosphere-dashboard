# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port for Dash
EXPOSE 8050

# Use gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
