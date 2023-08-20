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
    # Create the feelings table
    op.create_table(
        'feelings',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )

    # Adjust the strains table to fit the new model
    op.create_table(
        'strains',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('strain_type', sa.String, nullable=False),
        sa.Column('flavors', sa.String, nullable=True),
        sa.Column('helps_with', sa.String, nullable=True),
        sa.Column('thc_level', sa.String, nullable=True),
        sa.Column('dominant_terpene', sa.String, nullable=True)
    )

    # Create the strain_feeling association table
    op.create_table(
        'strain_feeling',
        sa.Column('strain_id', sa.INTEGER, sa.ForeignKey('strains.id'), primary_key=True),
        sa.Column('feeling_id', sa.INTEGER, sa.ForeignKey('feelings.id'), primary_key=True)
    )

def downgrade() -> None:
    op.drop_table('strain_feeling')
    op.drop_table('strains')
    op.drop_table('feelings')


