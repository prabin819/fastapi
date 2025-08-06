"""create_posts_table

Revision ID: 48eef72d2416
Revises: 
Create Date: 2025-08-06 13:04:41.412682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48eef72d2416'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     pass


# def downgrade() -> None:
#     """Downgrade schema."""
#     pass

def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
