# Python Image
FROM python:3.12.3-slim-bookworm

# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Set working directory
WORKDIR /home/app/web

# Install system dependecies for GDAL and posgreSQL (in Ubuntu)
RUN apt-get update && apt-get Install -y \
    gcc \
    g++ \
    gdal-bin \
    libgdal-dev \
    && apt-get clean \
    && rm rf /var/lib/apt/lists/*

# install the python dependencies 
RUN pip insall --upgrade pip 
COPY requirements.text .
RUN pip install --no-cache-dir -r requirements.txt 

#  

