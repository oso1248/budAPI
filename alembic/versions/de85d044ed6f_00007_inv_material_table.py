"""00007_inv_material_table

Revision ID: de85d044ed6f
Revises: e445ddecb1ae
Create Date: 2022-01-24 07:29:15.676029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de85d044ed6f'
down_revision = 'e445ddecb1ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inv_material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_pallets', sa.Integer(), nullable=False),
    sa.Column('total_units', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('total_per_unit', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('total_end', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('inv_uuid', sa.String(), nullable=False),
    sa.Column('id_commodity', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_commodity'], ['commodities.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inv_material')
    # ### end Alembic commands ###