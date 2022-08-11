"""empty message

Revision ID: 2fb916432f43
Revises: 
Create Date: 2022-08-11 20:56:29.236306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2fb916432f43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
                    sa.Column('avatar', postgresql.BYTEA(), autoincrement=False, nullable=True),
                    sa.Column('sex', postgresql.ENUM('man', 'woman', name='sex__'), autoincrement=False, nullable=True),
                    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key')
                    )
    op.create_table('avatars',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('avatar', sa.String(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"))
                    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
