FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /framework

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    -r requirements.txt

COPY .  .

RUN mkdir -p \
    reports/allure-results \
    reports/logs \
    reports/screenshots \
    test-results

CMD ["python", "-m", "pytest", "-m", "smoke or api", "--browser", "chromium", "-v"]