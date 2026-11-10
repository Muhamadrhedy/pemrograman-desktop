
from database import koneksi
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation, ForeignKeyViolation


class KaryawanRepository:

    def semua(self, cari="", hanya_aktif=False):
        with koneksi() as db:
            with db.cursor(row_factory=dict_row) as cur:

                sql = """
                    SELECT *
                    FROM karyawan
                    WHERE (
                        nik ILIKE %s
                        OR nama ILIKE %s
                    )
                """

                params = [f"%{cari}%", f"%{cari}%"]

                if hanya_aktif:
                    sql += " AND aktif = TRUE"

                sql += " ORDER BY nama, id"

                cur.execute(sql, params)

                return cur.fetchall()

    def simpan(self, m, id_karyawan=None):

        data = (
            m.nik,
            m.nama,
            m.jabatan,
            m.gaji_pokok,
            m.tunjangan,
            bool(m.aktif)
        )

        try:
            with koneksi() as db:
                with db.cursor() as cur:

                    if id_karyawan is None:

                        cur.execute("""
                            INSERT INTO karyawan (
                                nik,
                                nama,
                                jabatan,
                                gaji_pokok,
                                tunjangan,
                                aktif
                            )
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, data)

                    else:

                        cur.execute("""
                            SELECT id
                            FROM karyawan
                            WHERE id = %s
                            FOR UPDATE
                        """, (id_karyawan,))

                        if cur.fetchone() is None:
                            raise ValueError(
                                "Karyawan tidak ditemukan. Muat ulang data."
                            )

                        cur.execute("""
                            UPDATE karyawan
                            SET
                                nik = %s,
                                nama = %s,
                                jabatan = %s,
                                gaji_pokok = %s,
                                tunjangan = %s,
                                aktif = %s
                            WHERE id = %s
                        """, data + (id_karyawan,))

        except UniqueViolation as exc:

            if exc.diag.constraint_name == "karyawan_nik_key":
                raise ValueError(
                    "NIK internal sudah digunakan."
                ) from exc

            raise

    def hapus(self, id_karyawan):

        try:
            with koneksi() as db:
                with db.cursor() as cur:

                    cur.execute("""
                        DELETE FROM karyawan
                        WHERE id = %s
                    """, (id_karyawan,))

                    if cur.rowcount == 0:
                        raise ValueError(
                            "Karyawan tidak ditemukan."
                        )

        except ForeignKeyViolation as exc:

            raise ValueError(
                "Karyawan memiliki riwayat gaji. "
                "Ubah status menjadi nonaktif, jangan dihapus."
            ) from exc
