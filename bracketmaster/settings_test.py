"""Configurações isoladas para executar a suíte de testes com SQLite."""

import os

# settings.py exige essas variáveis durante a importação, mesmo que o banco
# seja substituído logo abaixo. setdefault preserva valores já definidos.
TEST_ENV = {
    "SECRET_KEY": "chave-insegura-apenas-para-testes",
    "DEFAULT_FROM_EMAIL": "testes@example.com",
    "BREVO_API_KEY": "test-key",
    "DB_NAME": "bracketmaster_test",
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DEBUG": "False",
    "ALLOWED_HOSTS": "localhost,127.0.0.1",
}

for key, value in TEST_ENV.items():
    os.environ.setdefault(key, value)

from .settings import *  # noqa: E402,F403

DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
