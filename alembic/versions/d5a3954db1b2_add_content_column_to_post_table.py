"""add content column to post table

Revision ID: d5a3954db1b2
Revises: 3998fcb74510
Create Date: 2024-08-08 10:08:29.077440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a3954db1b2'
down_revision: Union[str, None] = '3998fcb74510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
