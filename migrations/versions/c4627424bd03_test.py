"""test

Revision ID: c4627424bd03
Revises: 2f9683fdc191
Create Date: 2025-04-21 22:51:57.529739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4627424bd03'
down_revision: Union[str, None] = '2f9683fdc191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
