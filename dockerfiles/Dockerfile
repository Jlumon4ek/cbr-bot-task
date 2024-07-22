# Use the official Python image as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the 'app' directory from the host into the container at /usr/src/app
COPY ./app /usr/src/app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/requirements.txt