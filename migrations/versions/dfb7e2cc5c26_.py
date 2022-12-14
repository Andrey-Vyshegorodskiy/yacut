"""empty message

Revision ID: dfb7e2cc5c26
Revises: 
Create Date: 2022-10-12 16:22:28.484963

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dfb7e2cc5c26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URL_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=256), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_URL_map_timestamp'), 'URL_map', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_URL_map_timestamp'), table_name='URL_map')
    op.drop_table('URL_map')
    # ### end Alembic commands ###
