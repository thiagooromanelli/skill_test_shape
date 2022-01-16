"""empty message

Revision ID: da066c65cbf7
Revises: f98c4e43bdc5
Create Date: 2022-01-15 22:22:01.068731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da066c65cbf7'
down_revision = 'f98c4e43bdc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operation_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('equipment_code', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_code'], ['vessel_equipments.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation_orders')
    # ### end Alembic commands ###
