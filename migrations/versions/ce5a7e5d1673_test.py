"""test

Revision ID: ce5a7e5d1673
Revises: e7a51bfa34e2
Create Date: 2025-04-21 23:01:58.063303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce5a7e5d1673'
down_revision: Union[str, None] = 'e7a51bfa34e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
