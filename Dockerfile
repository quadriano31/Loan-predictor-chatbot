# Use the official Python base image
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
  python3-pip

# Copy the code files to the container
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port on which your Flask app runs
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["python", "app.py","-h", "0.0.0.0", "-p", "5000"]
