"""add second pk to Emloyee - last_name

Revision ID: 9c6944fc1af8
Revises: db319dcbe5d3
Create Date: 2023-09-17 18:48:35.196472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c6944fc1af8'
down_revision: Union[str, None] = 'db319dcbe5d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###