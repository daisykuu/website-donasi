import pandas as pd
from werkzeug.security import generate_password_hash
from app import app
from models import db, AdminPerpus

# Baca file Excel
df = pd.read_excel("DATA PERPUSDES & TBM.xlsx")

# Hilangkan spasi depan-belakang di semua nama kolom agar tidak error
df.columns = df.columns.str.strip()

with app.app_context():
    for index, row in df.iterrows():
        try:
            # Ambil kolom yang sudah dibersihkan namanya
            nama_perpus = str(row['NAMA PESPUSTAKAAN']).strip()
            desa = str(row['DESA/KEL']).replace("Desa ", "").replace("Kelurahan ", "").strip()
            kecamatan = str(row['KECAMATAN']).strip()

            # Buat username dan password sederhana
            username = nama_perpus.lower().replace(" ", "_") + "_" + kecamatan.lower()
            password_plain = desa.lower().replace(" ", "") + "123"
            password_hashed = generate_password_hash(password_plain)

            # Cek apakah username sudah ada
            if AdminPerpus.query.filter_by(username=username).first():
                print(f"❗ Username '{username}' sudah ada, dilewati.")
                continue

            # Tambahkan ke database
            admin = AdminPerpus(
                nama_perpus=nama_perpus,
                kecamatan=kecamatan,
                desa=desa,
                username=username,
                password_hash=password_hashed
            )
            db.session.add(admin)

        except Exception as e:
            print(f"❌ Error pada baris {index + 2}: {e}")

    db.session.commit()
    print("✅ Semua data perpustakaan berhasil dimasukkan ke database.")
