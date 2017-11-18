"""empty message

Revision ID: 192c6c1600f9
Revises:
Create Date: 2017-11-18 06:23:47.743490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192c6c1600f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column('blog_items', 'timestamp', existing_type=sa.Date, type_=sa.DateTime)

def downgrade():
    op.alter_column('blog_items', 'timestamp', existing_type=sa.DateTime, type_=sa.Date)
