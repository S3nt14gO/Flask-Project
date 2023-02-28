"""we test

Revision ID: 1cf7f6d35c38
Revises: a94c02e9c472
Create Date: 2023-02-22 22:44:58.178524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cf7f6d35c38'
down_revision = 'a94c02e9c472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('post_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_date', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###
