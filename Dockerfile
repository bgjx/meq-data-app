# Python Image
FROM python:3.13.3-slim-bookworm

# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Set working directory
WORKDIR /home/app/web