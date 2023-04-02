"""adding thc levels and dominant terpene columns

Revision ID: f33fbdf81b07
Revises: 32d18c480778
Create Date: 2023-04-02 11:25:53.763741

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f33fbdf81b07'
down_revision = '32d18c480778'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the new columns to the strains table
    op.add_column('strains', sa.Column('thc_level', sa.String(), nullable=True))
    op.add_column('strains', sa.Column('dominant_terpene', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the new columns from the strains table
    op.drop_column('strains', 'thc_level')
    op.drop_column('strains', 'dominant_terpene')
