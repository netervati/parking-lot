"""Fix Parking spot size.

Revision ID: 645d26e2cc0f
Revises: f8c42624ee1d
Create Date: 2022-02-10 03:20:46.302234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '645d26e2cc0f'
down_revision = 'f8c42624ee1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'distance', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'distance', 'spot', ['spot'], ['id'])
    op.create_foreign_key(None, 'distance', 'entrance', ['entrance'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'parking', 'spot', ['spot_id'], ['id'])
    op.create_foreign_key(None, 'parking', 'entrance', ['entrance_id'], ['id'])
    op.create_foreign_key(None, 'parking', 'user', ['created_by'], ['id'])
    op.drop_column('parking', 'updated_by')
    op.create_foreign_key(None, 'spot', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'user', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'spot', type_='foreignkey')
    op.add_column('parking', sa.Column('updated_by', mysql.VARCHAR(length=256), nullable=False))
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    # ### end Alembic commands ###
