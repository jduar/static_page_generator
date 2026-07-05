FROM python:3.12-slim AS base

WORKDIR /app

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid 1000 --create-home app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY templates ./templates
COPY static ./static

RUN chown -R app:app /app

FROM base AS dev
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
USER app
CMD ["watchfiles", "python src/main.py", "templates", "static", "src", "data/pages"]

# Default build target.
FROM base AS runtime
USER app
CMD ["python", "src/main.py"]
