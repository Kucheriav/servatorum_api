"""test

Revision ID: e7a51bfa34e2
Revises: c4627424bd03
Create Date: 2025-04-21 22:56:49.789009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7a51bfa34e2'
down_revision: Union[str, None] = 'c4627424bd03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
