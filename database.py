
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
import psycopg


@contextmanager
def koneksi():
    config = ConfigParser(interpolation=None)

    path = Path(__file__).resolve().with_name("config.ini")

    if not path.is_file():
        raise ValueError("File konfigurasi tidak ditemukan.")

    config.read(path, encoding="utf-8")

    if not config.has_section("postgresql"):
        raise ValueError(
            "Bagian [postgresql] tidak ditemukan pada config.ini."
        )

    c = config["postgresql"]

    db = psycopg.connect(
        host=c.get("host", "127.0.0.1"),
        port=c.getint("port", 5432),
        user=c.get("user", "postgres"),
        password=c.get("password", ""),
        dbname=c.get("database", "db_penggajian_modul5"),
        connect_timeout=5,
        autocommit=False,
    )

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
