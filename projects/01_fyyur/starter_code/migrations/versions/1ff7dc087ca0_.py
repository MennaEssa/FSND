"""empty message

Revision ID: 1ff7dc087ca0
Revises: 6f95484324af
Create Date: 2020-07-20 20:46:34.650535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff7dc087ca0'
down_revision = '6f95484324af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###
