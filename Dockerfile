FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY server.cert /app/server.cert
COPY server.key /app/server.key

EXPOSE 5000

ENV FLASK_APP=vision.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run", "--cert=server.cert", "--key=server.key"]