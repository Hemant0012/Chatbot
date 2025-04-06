# ✅ Start from an official Python base image with pip pre-installed
FROM python:3.11-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Copy all project files into the container
COPY . .

# ✅ Upgrade pip and install dependencies from requirements.txt
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# ✅ Expose the port FastAPI will run on
EXPOSE 8000

# ✅ Command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
