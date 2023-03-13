# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the Flask application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
