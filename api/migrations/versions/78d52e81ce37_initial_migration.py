"""Initial migration.

Revision ID: 78d52e81ce37
Revises: 
Create Date: 2024-12-09 09:50:21.923114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78d52e81ce37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tmdb', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('poster_path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tmdb', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mail'),
    sa.UniqueConstraint('username')
    )
    op.create_table('collection_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('borrowed', sa.Boolean(), nullable=True),
    sa.Column('borrowed_at', sa.DateTime(), nullable=True),
    sa.Column('borrowed_by', sa.String(), nullable=True),
    sa.Column('favorite', sa.Boolean(), nullable=True),
    sa.Column('in_wishlist', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('credits_film',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('character', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('film_collection',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('collection_item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collection_item_id'], ['collection_item.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
    sa.PrimaryKeyConstraint('film_id', 'collection_item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film_collection')
    op.drop_table('credits_film')
    op.drop_table('collection_item')
    op.drop_table('user')
    op.drop_table('person')
    op.drop_table('film')
    # ### end Alembic commands ###
