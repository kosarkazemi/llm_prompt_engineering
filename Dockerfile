# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip3 install poetry
# RUN poetry install --no-dev

# Copy the rest of the application code into the container at /app
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app when the container launches
CMD ["python", "app.py"]
