
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask requests
EXPOSE 5001 5002 5003
CMD ["python", "app.py"]