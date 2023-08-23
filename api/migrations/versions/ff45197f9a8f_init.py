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

    # Create the flavors table
    op.create_table(
        'flavors',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )

    # Create the helps_with table
    op.create_table(
        'helps_with',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )

    # Create the terpenes table
    op.create_table(
        'terpenes',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )

    # Create the strain_type table
    op.create_table(
        'types',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, unique=True, nullable=False)
    )

    # Adjust the strains table to fit the new model
    op.create_table(
        'strains',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('strain_type_id', sa.INTEGER, sa.ForeignKey('types.id'), nullable=False),  # Direct foreign key to types table
        sa.Column('thc_level', sa.String, nullable=True),
        sa.Column('dominant_terpene_id', sa.INTEGER, sa.ForeignKey('terpenes.id'), nullable=True)
    )

    # Create the strain_feeling association table
    op.create_table(
        'strain_feeling',
        sa.Column('strain_id', sa.INTEGER, sa.ForeignKey('strains.id'), primary_key=True),
        sa.Column('feeling_id', sa.INTEGER, sa.ForeignKey('feelings.id'), primary_key=True)
    )

    # Create the strain_flavor association table
    op.create_table(
        'strain_flavor',
        sa.Column('strain_id', sa.INTEGER, sa.ForeignKey('strains.id'), primary_key=True),
        sa.Column('flavor_id', sa.INTEGER, sa.ForeignKey('flavors.id'), primary_key=True)
    )

    # Create the strain_helps_with association table
    op.create_table(
        'strain_helps_with',
        sa.Column('strain_id', sa.INTEGER, sa.ForeignKey('strains.id'), primary_key=True),
        sa.Column('helps_with_id', sa.INTEGER, sa.ForeignKey('helps_with.id'), primary_key=True)
    )


def downgrade() -> None:
    op.drop_table('strain_feeling')
    op.drop_table('strain_flavor')
    op.drop_table('strain_helps_with')
    op.drop_table('strains')
    op.drop_table('feelings')
    op.drop_table('flavors')
    op.drop_table('helps_with')
    op.drop_table('terpenes')
    op.drop_table('types')


