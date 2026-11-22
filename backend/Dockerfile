FROM python:3.13-slim
WORKDIR /app
# Install the packages first: Docker caches this step, so code changes rebuild fast.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
# docker-compose mounts config.yml here.
ENV CONFIG_PATH=/config/config.yml
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
