from django.db.backends.base.base import BaseDatabaseWrapper

# Bypass MariaDB version check for compatibility with MariaDB < 10.6
BaseDatabaseWrapper.check_database_version_supported = lambda self: None
