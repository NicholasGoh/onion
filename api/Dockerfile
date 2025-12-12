FROM ghcr.io/astral-sh/uv:python3.13-bookworm

RUN groupadd -g 1000 user && \
  useradd -u 1000 -g 1000 -m -s /bin/bash user

RUN apt-get update && apt-get install -y --no-install-recommends curl
ENV UV_PROJECT_ENVIRONMENT=/opt/venv/.venv
ENV PATH=${UV_PROJECT_ENVIRONMENT}/bin:$PATH
USER user
WORKDIR /opt/venv

COPY ./api/uv.lock ./api/pyproject.toml ./
RUN uv sync --frozen && rm ./uv.lock ./pyproject.toml
COPY ./api /app
WORKDIR /app
