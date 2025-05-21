# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port and environment
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# Start the server
CMD ["flask", "run"]
# Use the following command to build the Docker image
# docker build -t flask-app .   
# Use the following command to run the Docker container
# docker run -p 5000:5000 flask-app
