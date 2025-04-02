"""Add DB

Revision ID: f66a729075a7
Revises: 6ddfeb2c7b6d
Create Date: 2025-03-28 17:25:57.510236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f66a729075a7'
down_revision: Union[str, None] = '6ddfeb2c7b6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
