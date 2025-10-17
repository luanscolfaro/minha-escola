"""Escola project package.

Provides a lightweight fallback to PyMySQL on environments
where mysqlclient (MySQLdb) wheels are not available (e.g., Windows + Py3.13).
The settings keep ENGINE='django.db.backends.mysql'. If MySQLdb isn't present,
we install PyMySQL as MySQLdb automatically.
"""

try:  # prefer native MySQLdb (mysqlclient)
    import MySQLdb  # type: ignore
except Exception:  # fall back to PyMySQL if available
    try:
        import pymysql  # type: ignore

        pymysql.install_as_MySQLdb()
    except Exception:
        # No MySQL backend available; if DB_ENGINE=mysql, Django will error at runtime.
        # On SQLite runs, this is harmless.
        pass
