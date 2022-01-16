"""empty message

Revision ID: f98c4e43bdc5
Revises: 0884d487c294
Create Date: 2022-01-15 19:47:25.742287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f98c4e43bdc5'
down_revision = '0884d487c294'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'vessel_equipments', 'vessels', ['vessel_code'], ['code'])
    op.drop_constraint('vessels_code_key', 'vessels', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('vessels_code_key', 'vessels', ['code'])
    op.drop_constraint(None, 'vessel_equipments', type_='foreignkey')
    # ### end Alembic commands ###
