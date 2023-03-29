"""init

Revision ID: ff45197f9a8f
Revises: 
Create Date: 2023-03-29 11:31:00.179360

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'ff45197f9a8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create tables for Strains
    op.create_table('strains',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('strain_type', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('strains')

