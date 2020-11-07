"""alter pubs

Revision ID: 0088b1aff5a4
Revises: 951d8f1d4d20
Create Date: 2020-11-07 15:25:38.936687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0088b1aff5a4'
down_revision = '951d8f1d4d20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pubs', sa.Column('is_channel', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pubs', 'is_channel')
    # ### end Alembic commands ###