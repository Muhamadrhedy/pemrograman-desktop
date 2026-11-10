
import psycopg

def test_postgres_connection():
    connection = None

    try:
        connection = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="praktikum",
            user="postgres",
            password="root"
        )

        print("Berhasil terhubung ke PostgreSQL!")

        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print("PostgreSQL Version:", version[0])

        cursor.execute("SELECT current_database();")
        database = cursor.fetchone()

        print("Database aktif:", database[0])

        cursor.close()

    except psycopg.Error as error:
        print("Gagal terhubung:", error)

    finally:
        if connection is not None:
            connection.close()
            print("Koneksi ditutup.")

if __name__ == "__main__":
    test_postgres_connection()
