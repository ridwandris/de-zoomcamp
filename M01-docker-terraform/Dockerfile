# Use the official Python image from the Docker Hub, 
# specifically the Alpine version for a smaller image size
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Set the working directory to /app, which is where our project files will be located
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Now we copy from the perspective of the project root
COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

# Copy the pipeline script specifically from the module folder
COPY M01-docker-terraform/injest_data.py .

ENTRYPOINT ["python", "injest_data.py"]