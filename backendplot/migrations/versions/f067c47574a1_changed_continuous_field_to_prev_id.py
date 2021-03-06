"""Changed continuous field to prev_id.

Revision ID: f067c47574a1
Revises: 555541c2f7ec
Create Date: 2022-02-08 11:32:44.635338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f067c47574a1'
down_revision = '555541c2f7ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'distance', 'spot', ['spot'], ['id'])
    op.create_foreign_key(None, 'distance', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'distance', 'entrance', ['entrance'], ['id'])
    op.create_foreign_key(None, 'distance', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'entrance', 'user', ['created_by'], ['id'])
    op.add_column('parking', sa.Column('prev_id', sa.String(length=256), nullable=True))
    op.create_foreign_key(None, 'parking', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'parking', 'spot', ['spot_size'], ['id'])
    op.create_foreign_key(None, 'parking', 'spot', ['spot_id'], ['id'])
    op.create_foreign_key(None, 'parking', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'parking', 'entrance', ['entrance_id'], ['id'])
    op.drop_column('parking', 'continuous')
    op.create_foreign_key(None, 'spot', 'user', ['updated_by'], ['id'])
    op.create_foreign_key(None, 'spot', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'spot', type_='foreignkey')
    op.drop_constraint(None, 'spot', type_='foreignkey')
    op.add_column('parking', sa.Column('continuous', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_constraint(None, 'parking', type_='foreignkey')
    op.drop_column('parking', 'prev_id')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'entrance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    op.drop_constraint(None, 'distance', type_='foreignkey')
    # ### end Alembic commands ###
