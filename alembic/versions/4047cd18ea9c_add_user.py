"""Add User

Revision ID: 4047cd18ea9c
Revises: f66a729075a7
Create Date: 2025-03-28 17:29:46.395636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4047cd18ea9c'
down_revision: Union[str, None] = 'f66a729075a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
