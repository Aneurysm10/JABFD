"""remove removed_by from moderation_case

Revision ID: 7ab9957da77d
Revises: 543700071a47
Create Date: 2026-09-24 09:51:12.805486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ab9957da77d'
down_revision: Union[str, Sequence[str], None] = '543700071a47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
