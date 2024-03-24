"""empty message

Revision ID: 322b046f20bb
Revises: 728be9dc90dd
Create Date: 2023-09-17 19:45:46.922872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '322b046f20bb'
down_revision: Union[str, None] = '728be9dc90dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('last_name', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employees', 'last_name')
    # ### end Alembic commands ###
