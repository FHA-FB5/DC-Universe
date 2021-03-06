"""create games table

Revision ID: f1a5ab97b1db
Revises: 410c6b08a575
Create Date: 2020-10-29 15:54:42.221251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a5ab97b1db'
down_revision = '410c6b08a575'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('role', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    # ### end Alembic commands ###
