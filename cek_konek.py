from database import koneksi

with koneksi() as db:
    with db.cursor() as cur:
        cur.execute("""
            SELECT current_database(), version();
        """)

        hasil = cur.fetchone()

        print("Database:", hasil[0])
        print("Versi PostgreSQL:", hasil[1])