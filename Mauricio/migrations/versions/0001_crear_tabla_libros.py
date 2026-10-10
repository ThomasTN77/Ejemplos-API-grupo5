import sqlalchemy as sa
from alembic import op

revision = "0001_libros"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "libros",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("titulo", sa.String(length=150), nullable=False),
        sa.Column("autor", sa.String(length=120), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=False),
        sa.Column("disponible", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade():
    op.drop_table("libros")
