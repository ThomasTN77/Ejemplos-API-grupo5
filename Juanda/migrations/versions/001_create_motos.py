"""Create the motos table."""

from alembic import op
import sqlalchemy as sa


revision = "001_create_motos"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "motos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("marca", sa.String(length=80), nullable=False),
        sa.Column("modelo", sa.String(length=120), nullable=False),
        sa.Column("cilindraje", sa.Integer(), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("motos")