# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Add current directory code to /usr/src/app in container
ADD . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]