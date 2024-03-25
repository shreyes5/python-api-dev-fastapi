"""add content column to post table

Revision ID: 74cebb24250a
Revises: b99dd71a8929
Create Date: 2024-03-25 16:16:03.185735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74cebb24250a'
down_revision: Union[str, None] = 'b99dd71a8929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
