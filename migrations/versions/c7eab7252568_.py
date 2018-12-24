"""empty message

Revision ID: c7eab7252568
Revises: 9fccd76b7def
Create Date: 2018-12-24 13:25:34.120993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7eab7252568'
down_revision = '9fccd76b7def'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_daily_meditations_date'), 'daily_meditations', ['date'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_daily_meditations_date'), table_name='daily_meditations')
    # ### end Alembic commands ###