FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY . /app
CMD ["python", "run_assessment.py", "--agent-url", "http://candidate-agent:8000", "--api-url", "http://mock-api:8001", "--trials", "3", "--report-dir", "/reports/latest"]
