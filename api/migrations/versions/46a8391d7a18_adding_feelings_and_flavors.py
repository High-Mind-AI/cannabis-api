"""adding feelings and flavors

Revision ID: 46a8391d7a18
Revises: ff45197f9a8f
Create Date: 2023-04-02 01:40:43.353534

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '46a8391d7a18'
down_revision = 'ff45197f9a8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the new columns to the strains table
    op.add_column('strains', sa.Column('feelings', sa.String(), nullable=True))
    op.add_column('strains', sa.Column('flavors', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the new columns from the strains table
    op.drop_column('strains', 'feelings')
    op.drop_column('strains', 'flavors')
