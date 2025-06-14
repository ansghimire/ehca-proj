#!/usr/bin/env python
import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'apps')))

def main():
    """Run administrative tasks."""
    # Set the settings module from environment variable; default to development
    settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
