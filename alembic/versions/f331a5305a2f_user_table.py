"""user table

Revision ID: f331a5305a2f
Revises: d61201b12eb2
Create Date: 2023-09-04 15:52:59.289862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f331a5305a2f'
down_revision: Union[str, None] = 'd61201b12eb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
