FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends redis-tools \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" bot \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" bot \
  && chown bot:bot -R /app

COPY --chown=bot:bot . .
RUN uv pip install --system --no-cache -r pyproject.toml

USER bot
