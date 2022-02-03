"""Designed Entrance model.

Revision ID: 4c7245c2e8c5
Revises: 45bca055995a
Create Date: 2022-02-04 03:09:18.975575

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4c7245c2e8c5'
down_revision = '45bca055995a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entrance',
    sa.Column('id', sa.String(length=256), autoincrement=False, nullable=False),
    sa.Column('label', sa.String(length=20), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(length=256), nullable=False),
    sa.Column('updated_by', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label')
    )
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    op.drop_table('entrance')
    # ### end Alembic commands ###