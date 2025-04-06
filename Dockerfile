# ✅ Use a stable Python image with pip
FROM python:3.11-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Copy files
COPY . .

# ✅ Ensure system packages are updated and dependencies are installed
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev && \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ✅ Expose the port
EXPOSE 8000

# ✅ Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
