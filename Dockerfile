# Set Base Image
FROM python:3.7

# Set Working directory
WORKDIR /src

# Copy Requirements to working directory
COPY _requirements.txt

# Install Dependencies
RUN pip install -r _requirements.txt

# Copy content of local src dir to working directory
COPY src/.