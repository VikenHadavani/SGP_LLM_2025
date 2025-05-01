FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

COPY server.cert /app/server.cert
COPY server.key /app/server.key

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "vision.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.sslCertFile=/app/server.cert", "--server.sslKeyFile=/app/server.key"]