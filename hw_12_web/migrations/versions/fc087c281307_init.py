"""Init

Revision ID: fc087c281307
Revises: 76a41421ecf2
Create Date: 2023-05-07 22:21:25.572890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc087c281307'
down_revision = '76a41421ecf2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_contacts_phone_number', table_name='contacts')
    op.create_index(op.f('ix_contacts_phone_number'), 'contacts', ['phone_number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contacts_phone_number'), table_name='contacts')
    op.create_index('ix_contacts_phone_number', 'contacts', ['phone_number'], unique=False)
    # ### end Alembic commands ###