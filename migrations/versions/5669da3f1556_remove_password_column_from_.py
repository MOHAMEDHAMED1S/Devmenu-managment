"""Remove password column from subscriptions table

Revision ID: 5669da3f1556
Revises: 603e6e46243b
Create Date: 2025-04-07 07:02:30.445250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5669da3f1556'
down_revision = '603e6e46243b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
