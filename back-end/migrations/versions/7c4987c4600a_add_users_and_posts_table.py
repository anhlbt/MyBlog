"""add users and posts table

Revision ID: 7c4987c4600a
Revises: 
Create Date: 2018-11-09 20:56:48.786237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext import mutable
import json


# revision identifiers, used by Alembic.
revision = '7c4987c4600a'
down_revision = None
branch_labels = None
depends_on = None

class JsonEncodedDict(sa.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = sa.Text()

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    # avatar = db.Column(db.String(20), nullable=True)
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('topic', sa.String(length=64), nullable=True),  #ebook or ...
    sa.Column('image', sa.PickleType(), nullable=True),
    sa.Column('tags', sa.String(length=500), nullable=True),
    sa.Column('link_', sa.String(length=500), nullable=True),
    sa.Column('source', sa.String(length=500), nullable=True),
    sa.Column('audio_links', sa.PickleType(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('json_book', JsonEncodedDict),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_timestamp'), 'posts', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_timestamp'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
