"""adding helps_with column

Revision ID: 32d18c480778
Revises: 46a8391d7a18
Create Date: 2023-04-02 10:45:37.275336

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '32d18c480778'
down_revision = '46a8391d7a18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the new columns to the strains table
    op.add_column('strains', sa.Column('helps_with', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the new columns from the strains table
    op.drop_column('strains', 'helps_with')
