import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave de segurança (SECRET_KEY)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dominus-sys-chave-local-desenvolvimento')

# Ativa modo de depuração se não estiver em ambiente de produção
DEBUG = os.environ.get('ENVIRONMENT') != 'PRODUCTION'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']


# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Aplicação principal do DOMINUS SYS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# CONFIGURAÇÃO DE BANCO DE DADOS DINÂMICO (PASSO 2 - DIA 41)
PRODUCAO = os.environ.get('ENVIRONMENT') == 'PRODUCTION'

if PRODUCAO:
    # SGBD PostgreSQL para Produção em Nuvem
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'db_dominus'),
            'USER': os.environ.get('DB_USER', 'usr_dominus'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'SenhaSeguraPostgres'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    # Banco SQLite3 leve para Desenvolvimento Local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Validação de Senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalização e Fuso Horário
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_TZ = True


# Arquivos Estáticos
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Redirecionamento de Autenticação
LOGIN_REDIRECT_URL = 'painel'
LOGOUT_REDIRECT_URL = 'painel'

# Tipo padrão de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'