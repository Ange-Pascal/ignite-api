# --- IMAGE DE BASE ---
FROM python:3.12-alpine

LABEL maintainer="apdeveloper.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/py/bin:$PATH"

# --- DÉPENDANCES SYSTÈME ---
RUN apk add --no-cache postgresql-libs libpq bash curl

# Dépendances de build temporaires
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev

# --- DOSSIER DE TRAVAIL ---
WORKDIR /app

# --- INSTALLATION DES DEPENDANCES PYTHON ---
COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt --prefer-binary && \
    rm -rf /tmp && \
    apk del .build-deps

# --- COPIE DU CODE ---
COPY ./app /app
COPY entrypoint.sh /entrypoint.sh

# --- PERMISSIONS ---
RUN chmod +x /entrypoint.sh && \
    adduser -D -H django-user && \
    chown -R django-user:django-user /app

USER django-user

# --- PORT (Cloud Run) ---
EXPOSE 8080

# --- COMMANDE DE DÉMARRAGE ---
ENTRYPOINT ["/entrypoint.sh"]
