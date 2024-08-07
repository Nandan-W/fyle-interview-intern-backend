# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
