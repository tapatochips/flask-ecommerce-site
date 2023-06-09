"""empty message

Revision ID: 36236ddd09c0
Revises: af39fe50e5cf
Create Date: 2023-04-24 16:59:29.744505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36236ddd09c0'
down_revision = 'af39fe50e5cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
