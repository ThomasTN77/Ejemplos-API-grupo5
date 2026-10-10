"""Create the animales table."""

from alembic import op
import sqlalchemy as sa


revision = "001_create_animales"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "animales",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("especie", sa.String(length=120), nullable=False),
        sa.Column("edad", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("animales")