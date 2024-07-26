# Use the official Python image as the base image
FROM python:3.12.2

# Set the working directory
WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt and install the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# # Run the FastAPI app using uvicorn
# CMD ["uvicorn", "App.Main:app", "--host", "0.0.0.0", "--port", "8000"]

# # Run the FastAPI app using gunicorn
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "App.Main:app", "--bind", "0.0.0.0:8000"]
