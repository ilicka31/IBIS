FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install Flask==2.3.2 paho-mqtt==1.6.1 requests==2.31.0 PyYAML==6.0
EXPOSE 5001
CMD ["python", "main.py"]
