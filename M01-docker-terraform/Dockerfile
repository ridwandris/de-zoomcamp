FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Now we copy from the perspective of the project root
COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

# Copy the pipeline script specifically from the module folder
COPY M01-docker-terraform/pipeline.py .

ENTRYPOINT ["python", "pipeline.py" ]