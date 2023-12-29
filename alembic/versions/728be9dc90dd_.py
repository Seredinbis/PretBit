"""empty message

Revision ID: 728be9dc90dd
Revises: 7ad1a5fc4868
Create Date: 2023-09-17 19:44:57.908375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '728be9dc90dd'
down_revision: Union[str, None] = '7ad1a5fc4868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'last_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('last_name', sa.VARCHAR(length=40), autoincrement=False, nullable=False))
    # ### end Alembic commands ###