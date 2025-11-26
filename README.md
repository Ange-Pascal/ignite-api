# ignite-api
Ignite LMS website api


# -------------------------------------------------------------
# 1) Image de base
# -------------------------------------------------------------
# On utilise Python 3.14 sur Alpine Linux 3.21
# Alpine = image légère → idéale pour réduire la taille du Docker final.
FROM python:3.14-alpine3.21



# -------------------------------------------------------------
# 2) Metadata
# -------------------------------------------------------------
# Simple label pour identifier le mainteneur (facultatif mais utile)
LABEL maintainer="apdeveloper.com"



# -------------------------------------------------------------
# 3) Variables d'environnement
# -------------------------------------------------------------
# PYTHONUNBUFFERED=1 → empêche Python de bufferiser les logs.
# Résultat : les logs Django s’affichent immédiatement dans la console.
ENV PYTHONUNBUFFERED 1



# -------------------------------------------------------------
# 4) Copie des fichiers nécessaires à l'installation des dépendances
# -------------------------------------------------------------
# On copie les requirements dans /tmp (bonne pratique pour Docker).
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copie du code de l'app dans /app
COPY ./app /app



# -------------------------------------------------------------
# 5) Définir le dossier de travail
# -------------------------------------------------------------
# Toutes les commandes suivantes (RUN, CMD…) seront exécutées dans /app.
WORKDIR /app



# -------------------------------------------------------------
# 6) Port exposé
# -------------------------------------------------------------
# Par défaut Django tourne sur le port 8000.
EXPOSE 8000



# -------------------------------------------------------------
# 7) Arguments de build
# -------------------------------------------------------------
# DEV=false → Par défaut, on n’installe pas les packages de développement.
# Pour activer : docker build --build-arg DEV=true .
ARG DEV=false



# -------------------------------------------------------------
# 8) Installation de Python + PostgreSQL client + dépendances
# -------------------------------------------------------------
RUN python -m venv /py && \                             # Crée un environnement virtuel dans /py
    /py/bin/pip install --upgrade pip && \              # Met à jour pip

    # Installations nécessaires au client PostgreSQL
    apk add --update --no-cache postgresql-client && \  # Install client postgres (psql)

    # Installation des dépendances système nécessaires pour compiler
    # psycopg (non-binary), pillow, et autres libs compilées.
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \

    # Installation des dépendances Python officielles
    /py/bin/pip install -r /tmp/requirements.txt && \

    # Si ARG DEV=true → installer les packages de développement
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \

    # Supprimer le dossier /tmp pour alléger l'image finale
    rm -rf /tmp && \

    # Supprimer les dépendances utilisées uniquement pour la compilation
    apk del .tmp-build-deps && \

    # Ajout d'un utilisateur non-root pour raisons de sécurité
    adduser \
        --disabled-password \   # Pas de mot de passe
        --no-create-home \      # Pas de dossier personnel
        django-user             # Nom du user



# -------------------------------------------------------------
# 9) Ajouter le venv au PATH
# -------------------------------------------------------------
# Permet d'utiliser "python" et "pip" directement sans écrire /py/bin/...
ENV PATH="/py/bin:$PATH"



# -------------------------------------------------------------
# 10) Exécuter le container sous un utilisateur sécurisé
# -------------------------------------------------------------
# On évite d'exécuter Django en root → bonne pratique devops / sécurité.
USER django-user


#Docker compose explication


services:
  # -------------------------------------------------------------
  # 1) SERVICE : APP (Django)
  # -------------------------------------------------------------
  app:
    # Section BUILD : indique comment construire l'image Docker
    build:
      context: .             # Le Dockerfile se trouve dans le dossier actuel
      args:
        - DEV=true           # Passe ARG DEV=true au Dockerfile (installe deps dev)

    # -------------------------------------------------------------
    # Ports exposés
    # -------------------------------------------------------------
    ports:
      - "8000:8000"          # Host port 8000 → Container port 8000 (Django)

    # -------------------------------------------------------------
    # Volume local monté dans le conteneur
    # -------------------------------------------------------------
    volumes:
      - ./app:/app           # Synchronise ton code local avec le container
                             # Idéal pour le développement sans rebuild

    # -------------------------------------------------------------
    # Commande exécutée au démarrage du conteneur
    # -------------------------------------------------------------
    command: >
      sh -c "
        python manage.py wait_for_db &&
        python manage.py migrate &&
        python manage.py runserver 0.0.0.0:8000
      "
      # 1) wait_for_db : script pour attendre PostgreSQL avant de lancer Django
      # 2) migrate : applique les migrations
      # 3) runserver : démarre Django accessible depuis l'extérieur

    # -------------------------------------------------------------
    # Variables d'environnement pour config Django/PostgreSQL
    # -------------------------------------------------------------
    environment:
      - DB_HOST=db           # Hostname du service PostgreSQL
      - DB_NAME=devdb        # Nom de la base de données
      - DB_USER=devuser      # Utilisateur PostgreSQL
      - DB_PASS=changeme     # Mot de passe PostgreSQL

    # -------------------------------------------------------------
    # Dépendances entre services
    # -------------------------------------------------------------
    depends_on:
      - db                   # Démarre Django après PostgreSQL (ordre logique)



  # -------------------------------------------------------------
  # 2) SERVICE : DB (PostgreSQL)
  # -------------------------------------------------------------
  db:
    image: postgres:18-alpine  # Version PostgreSQL officielle + Alpine

    # -------------------------------------------------------------
    # Volume pour la persistance des données PostgreSQL
    # -------------------------------------------------------------
    volumes:
      - dev-db-data:/var/lib/postgresql/18/docker
      # Ce volume permet de garder la base même si le container est supprimé

    # -------------------------------------------------------------
    # Variables d'environnement pour initialiser PostgreSQL
    # -------------------------------------------------------------
    environment:
      - POSTGRES_DB=devdb         # Nom de la DB à créer au démarrage
      - POSTGRES_USER=devuser     # Utilisateur par défaut
      - POSTGRES_PASSWORD=changeme  # Mot de passe par défaut



# -------------------------------------------------------------
# 3) Déclaration de VOLUMES persistants
# -------------------------------------------------------------
volumes:
  dev-db-data:                # Volume nommé pour PostgreSQL
