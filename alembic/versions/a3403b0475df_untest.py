"""untest

Revision ID: a3403b0475df
Revises: 073d64e5dcca
Create Date: 2023-09-16 18:27:50.731435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3403b0475df'
down_revision: Union[str, None] = '073d64e5dcca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('worktime', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('worktime', sa.Column('test', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
