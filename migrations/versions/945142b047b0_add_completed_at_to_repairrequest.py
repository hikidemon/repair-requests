"""Add completed_at to RepairRequest

Revision ID: 945142b047b0
Revises: 
Create Date: 2024-10-20 20:19:09.193316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '945142b047b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repair_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repair_request', schema=None) as batch_op:
        batch_op.drop_column('completed_at')

    # ### end Alembic commands ###
