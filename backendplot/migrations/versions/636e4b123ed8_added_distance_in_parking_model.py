"""Added distance in Parking model.

Revision ID: 636e4b123ed8
Revises: 609163271cf0
Create Date: 2022-02-07 06:08:16.613080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '636e4b123ed8'
down_revision = '609163271cf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'distance', 'entrance', ['entrance'], ['id'])
    op.create_foreign_key(None, 'distance', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'distance', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'distance', 'spot', ['spot'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['updated_by'], ['id'])
    op.add_column('parking', sa.Column('distance_distance', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'parking', 'spot', ['spot_id'], ['id'])
    op.create_foreign_key(None, 'parking', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'parking', 'spot', ['spot_size'], ['id'])
    op.create_foreign_key(None, 'parking', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'parking', 'entrance', ['entrance_id'], ['id'])
    op.create_foreign_key(None, 'spot', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'spot', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'spot', type_='foreignkey')
    op.drop_constraint(None, 'spot', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_column('parking', 'distance_distance')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    # ### end Alembic commands ###
