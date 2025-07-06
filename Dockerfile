FROM python:3.12-slim-bookworm
#install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app/app
RUN uv sync --locked

EXPOSE 8000

CMD [ "uv", "run", "fastapi", "run", "main.py", "--port", "8000"]