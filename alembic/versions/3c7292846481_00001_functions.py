"""00001_functions

Revision ID: 3c7292846481
Revises: 
Create Date: 2022-01-21 19:09:46.610739

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from api.config import settings
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '3c7292846481'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute("""
        CREATE OR REPLACE FUNCTION update_timestamp() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$;
    """)

    session.execute("SET TIMEZONE = 'America/Denver';")

    pass


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("DROP FUNCTION update_timestamp();")
    pass
