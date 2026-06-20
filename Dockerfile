# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Render uses
EXPOSE 10000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]