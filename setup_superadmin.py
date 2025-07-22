from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Buat tabel baru kalau belum ada
    db.create_all()

    # Cek apakah superadmin sudah ada
    existing_admin = User.query.filter_by(username='superadmin').first()
    if existing_admin:
        print("⚠️ Superadmin sudah ada.")
    else:
        # Buat akun superadmin baru
        user = User(
            username='superadmin',
            full_name='Super Admin',
            phone_number='081234567890',
            email='admin@lumajang.go.id',
            password=generate_password_hash('admin123'),
            role='superadmin'
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Superadmin berhasil dibuat.")
