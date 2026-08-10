#!/usr/bin/env python
"""Entry point para os comandos de gerenciamento do Django."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config_monitor.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar Django. Verifique se o ambiente virtual está ativado "
            "e se o pacote django está instalado."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
