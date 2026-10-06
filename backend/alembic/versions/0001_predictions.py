import sqlalchemy as sa

from alembic import op

revision = "0001_predictions"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("cancer_type", sa.String(length=40), nullable=False),
        sa.Column("stage", sa.Integer(), nullable=False),
        sa.Column("treatment", sa.String(length=40), nullable=False),
        sa.Column("biomarker", sa.Float(), nullable=False),
        sa.Column("response_probability", sa.Float(), nullable=False),
        sa.Column("predicted_response", sa.Boolean(), nullable=False),
        sa.Column("model_version", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("predictions")
