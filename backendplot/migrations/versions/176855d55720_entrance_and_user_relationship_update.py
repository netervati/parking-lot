"""Entrance and User Relationship update.

Revision ID: 176855d55720
Revises: 4c7245c2e8c5
Create Date: 2022-02-04 11:03:55.679792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '176855d55720'
down_revision = '4c7245c2e8c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'entrance', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    # ### end Alembic commands ###
