from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ac5af9d9678'
down_revision = '6d0be21a25fe'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Tambahkan kolom username sementara nullable=True
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=True))

    # ❗Isi kolom username dengan nilai sementara (misal: email sebagai username)
    op.execute("UPDATE user SET username = email")

    # ❗Setelah semua sudah punya data, ubah jadi NOT NULL dan kasih unique constraint
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username', existing_type=sa.String(length=50), nullable=False)
        batch_op.create_unique_constraint('uq_user_username', ['username'])


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.drop_column('username')
