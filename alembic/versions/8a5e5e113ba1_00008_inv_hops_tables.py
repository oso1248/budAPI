"""00008_inv_hops_tables

Revision ID: 8a5e5e113ba1
Revises: de85d044ed6f
Create Date: 2022-01-28 09:45:44.952957

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '8a5e5e113ba1'
down_revision = 'de85d044ed6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inv_last_brews',
                    sa.Column('inv_uuid', postgresql.UUID(
                        as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('bh_1', sa.String(), nullable=False),
                    sa.Column('bh_2', sa.String(), nullable=False),
                    sa.Column('created_by', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['created_by'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('inv_uuid')
                    )
    op.create_table('inv_hop',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('total_pallets', sa.Integer(), nullable=False),
                    sa.Column('total_units', sa.Numeric(
                        precision=9, scale=2), nullable=False),
                    sa.Column('total_per_unit', sa.Numeric(
                        precision=9, scale=2), nullable=False),
                    sa.Column('total_end', sa.Numeric(
                        precision=9, scale=2), nullable=False),
                    sa.Column('lot_number', sa.String(), nullable=False),
                    sa.Column('note', sa.String(), nullable=True),
                    sa.Column('inv_uuid', postgresql.UUID(
                        as_uuid=True), nullable=False),
                    sa.Column('id_commodity', sa.Integer(), nullable=False),
                    sa.Column('created_by', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['created_by'], ['users.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['id_commodity'], ['commodities.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['inv_uuid'], ['inv_last_brews.inv_uuid'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("""
        CREATE OR REPLACE FUNCTION delete_old_rows_inv_last_brews() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            DELETE FROM inv_last_brews WHERE created_at < NOW() - INTERVAL '1095 days';
        RETURN NULL;
        END;
        $$;
    """)
    session.execute("""
        CREATE TRIGGER trigger_delete_old_rows_inv_last_brews
        AFTER INSERT ON inv_last_brews
        EXECUTE PROCEDURE delete_old_rows_inv_last_brews();
    """)
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("""
        CREATE OR REPLACE FUNCTION delete_old_rows_inv_hop() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            DELETE FROM inv_hop WHERE created_at < NOW() - INTERVAL '1095 days';
        RETURN NULL;
        END;
        $$;
    """)
    session.execute("""
        CREATE TRIGGER trigger_delete_old_rows_inv_hop
        AFTER INSERT ON inv_hop
        EXECUTE PROCEDURE delete_old_rows_inv_hop();
    """)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inv_hop')
    op.drop_table('inv_last_brews')
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("DROP FUNCTION delete_old_rows_inv_last_brews();")
    session.execute("DROP FUNCTION delete_old_rows_inv_hop();")
    # ### end Alembic commands ###
