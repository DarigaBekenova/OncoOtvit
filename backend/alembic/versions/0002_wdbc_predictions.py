import sqlalchemy as sa

from alembic import op

revision = "0002_wdbc_predictions"
down_revision = "0001_predictions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("predictions")
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sample_name", sa.String(length=100), nullable=False),
        sa.Column("reference_class", sa.String(length=20), nullable=False),
        sa.Column("predicted_class", sa.String(length=20), nullable=False),
        sa.Column("malignant_probability", sa.Float(), nullable=False),
        sa.Column("model_version", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("predictions")
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
