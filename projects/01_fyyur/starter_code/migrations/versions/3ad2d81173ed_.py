"""empty message

Revision ID: 3ad2d81173ed
Revises: 0ba34d1c9fe5
Create Date: 2022-08-20 23:33:46.152382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad2d81173ed'
down_revision = '0ba34d1c9fe5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'website_link')
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'upcoming_shows_count')
    # ### end Alembic commands ###
