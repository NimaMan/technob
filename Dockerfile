# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /technob

# Copy the current directory contents into the container at /app
COPY . /technob

# Install any needed system packages. If you need some system packages, just add them to this list
RUN apt-get update && apt-get install -y \
    make \
    automake \
    gcc \
    g++ \
    python3-dev \
    gfortran \
    build-essential \
    wget

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables if needed (e.g., for configurations)
# ENV MY_VARIABLE=value
