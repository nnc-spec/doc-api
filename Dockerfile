# Use the official Python 3.9 image as the base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
