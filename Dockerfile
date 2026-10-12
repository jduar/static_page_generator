FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.25 /uv /bin/uv

WORKDIR /app

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid 1000 --create-home app

COPY pyproject.toml uv.lock .python-version ./
ARG UV_SYNC_FLAGS=--no-dev
RUN uv sync --frozen $UV_SYNC_FLAGS --no-cache

COPY src ./src
COPY example_content ./example_content

RUN chown -R app:app /app

ENV PATH="/app/.venv/bin:$PATH"

USER app
CMD ["python", "src/main.py"]
