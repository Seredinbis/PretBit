"""change nullbase in WorkTime.time

Revision ID: db319dcbe5d3
Revises: a3403b0475df
Create Date: 2023-09-17 16:47:57.659350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db319dcbe5d3'
down_revision: Union[str, None] = 'a3403b0475df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('worktime', 'time',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('worktime', 'time',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###
