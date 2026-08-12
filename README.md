# Projeto Semana 6 - Monitoramento e Financeiro

Este repositório contém uma aplicação Django (versão 6.1) com funcionalidades de monitoramento de servidores e um módulo financeiro simples.

Como preparar o ambiente

1. Criar e ativar um virtualenv (Windows PowerShell):

```powershell
python -m venv .venv
& ".venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
```

Executar o projeto

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Testes

```powershell
python manage.py test
```

Próximos passos sugeridos:
- Configurar CI (GitHub Actions) para rodar testes automaticamente.
- Adicionar documentação das APIs REST.
