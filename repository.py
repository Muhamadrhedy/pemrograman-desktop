
from database import koneksi
from model import hitung_gaji, periode_valid
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
                                nik, nama, jabatan,
                                gaji_pokok, tunjangan, aktif
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
                            SET nik = %s,
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


class GajiRepository:

    def simpan(self, id_karyawan, periode, jam, tarif, potongan):

        periode = periode_valid(periode)

        try:
            with koneksi() as db:
                with db.cursor(row_factory=dict_row) as cur:

                    # Ambil data karyawan dan kunci baris
                    cur.execute("""
                        SELECT *
                        FROM karyawan
                        WHERE id = %s
                        FOR UPDATE
                    """, (id_karyawan,))

                    k = cur.fetchone()

                    if k is None or not k["aktif"]:
                        raise ValueError(
                            "Karyawan tidak ada atau sudah nonaktif."
                        )

                    # Hitung penggajian
                    hasil = hitung_gaji(
                        k["gaji_pokok"],
                        k["tunjangan"],
                        jam,
                        tarif,
                        potongan
                    )

                    values = (
                        id_karyawan,
                        periode,
                        k["nik"],
                        k["nama"],
                        k["jabatan"],
                        hasil["gaji_pokok"],
                        hasil["tunjangan"],
                        hasil["jam_lembur"],
                        hasil["tarif_lembur"],
                        hasil["uang_lembur"],
                        hasil["potongan"],
                        hasil["bruto"],
                        hasil["netto"]
                    )

                    # Simpan dan ambil ID otomatis
                    cur.execute("""
                        INSERT INTO penggajian (
                            karyawan_id,
                            periode,
                            nik,
                            nama,
                            jabatan,
                            gaji_pokok,
                            tunjangan,
                            jam_lembur,
                            tarif_lembur,
                            uang_lembur,
                            potongan,
                            bruto,
                            netto
                        )
                        VALUES (
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        RETURNING id
                    """, values)

                    id_gaji = cur.fetchone()["id"]

                    return id_gaji

        except UniqueViolation as exc:
            if exc.diag.constraint_name == "uq_gaji_periode":
                raise ValueError(
                    "Gaji karyawan pada periode ini sudah tersimpan."
                ) from exc
            raise

    def semua(self, periode):

        periode = periode_valid(periode)

        with koneksi() as db:
            with db.cursor(row_factory=dict_row) as cur:

                cur.execute("""
                    SELECT *
                    FROM penggajian
                    WHERE periode = %s
                    ORDER BY nama, id
                """, (periode,))

                return cur.fetchall()

    def ringkasan(self, periode):

        periode = periode_valid(periode)

        with koneksi() as db:
            with db.cursor(row_factory=dict_row) as cur:

                cur.execute("""
                    SELECT COUNT(*) AS total
                    FROM karyawan
                    WHERE aktif = TRUE
                """)

                total = cur.fetchone()["total"]

                cur.execute("""
                    SELECT
                        COUNT(*) AS slip,
                        COALESCE(SUM(netto), 0) AS netto
                    FROM penggajian
                    WHERE periode = %s
                """, (periode,))

                hasil = cur.fetchone()

                return dict(
                    aktif=total,
                    **hasil
                )
