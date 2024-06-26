# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install ffmpeg and other necessary libraries for OpenCV
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Export the Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Run app.py when the container launches
CMD ["python", "src/main.py"]