"""July init

Revision ID: 436aff625488
Revises: 
Create Date: 2025-07-09 01:18:51.647618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '436aff625488'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_verification_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admin_verification_codes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_verification_codes_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_admin_verification_codes_phone'), ['phone'], unique=False)

    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('is_superadmin', sa.Boolean(), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('chat_id_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('administrator_name', sa.String(), nullable=True),
    sa.Column('administrator_surname', sa.String(), nullable=True),
    sa.Column('administrator_lastname', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('site', sa.String(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("phone ~ '^7[0-9]{10}$'", name='check_phone'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_companies_id'), ['id'], unique=False)

    op.create_table('foundations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('administrator_name', sa.String(), nullable=True),
    sa.Column('administrator_surname', sa.String(), nullable=True),
    sa.Column('administrator_lastname', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('site', sa.String(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("phone ~ '^7[0-9]{10}$'", name='check_phone'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('foundations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_foundations_id'), ['id'], unique=False)

    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('publication_date', sa.Date(), nullable=False),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spheres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_verification_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_verification_codes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_verification_codes_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_verification_codes_phone'), ['phone'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('helping', 'getting help', name='user_role_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('wallets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_type', sa.Enum('user', 'company', 'foundation', 'fundraising', name='wallet_owner_type_enum'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('owner_type', 'owner_id', name='unique_owner_wallet')
    )
    op.create_table('admin_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('valid_before', sa.DateTime(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_account_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company', sa.Integer(), nullable=True),
    sa.Column('inn', sa.String(), nullable=True),
    sa.Column('kpp', sa.String(), nullable=True),
    sa.Column('account_name', sa.String(), nullable=True),
    sa.Column('bank_account', sa.String(), nullable=True),
    sa.Column('cor_account', sa.String(), nullable=True),
    sa.Column('bik', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['company'], ['companies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company'),
    sa.UniqueConstraint('inn')
    )
    with op.batch_alter_table('company_account_details', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_company_account_details_id'), ['id'], unique=False)

    op.create_table('company_spheres',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('sphere_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['sphere_id'], ['spheres.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'sphere_id')
    )
    op.create_table('foundation_account_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('foundation', sa.Integer(), nullable=True),
    sa.Column('inn', sa.String(), nullable=True),
    sa.Column('kpp', sa.String(), nullable=True),
    sa.Column('account_name', sa.String(), nullable=True),
    sa.Column('bank_account', sa.String(), nullable=True),
    sa.Column('cor_account', sa.String(), nullable=True),
    sa.Column('bik', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['foundation'], ['foundations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inn')
    )
    with op.batch_alter_table('foundation_account_details', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_foundation_account_details_id'), ['id'], unique=False)

    op.create_table('foundation_spheres',
    sa.Column('foundation_id', sa.Integer(), nullable=False),
    sa.Column('sphere_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['foundation_id'], ['foundations.id'], ),
    sa.ForeignKeyConstraint(['sphere_id'], ['spheres.id'], ),
    sa.PrimaryKeyConstraint('foundation_id', 'sphere_id')
    )
    op.create_table('fundraising_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fundraise_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('file_type', sa.Enum('doc', 'photo', name='file_type_enum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['fundraise_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('fundraising_files', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_fundraising_files_id'), ['id'], unique=False)

    op.create_table('fundraisings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('goal_amount', sa.Float(), nullable=True),
    sa.Column('raised_amount', sa.Float(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('finish_date', sa.Date(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('finish_date > start_date'),
    sa.CheckConstraint('finish_date >= CURRENT_DATE'),
    sa.CheckConstraint('start_date >= CURRENT_DATE'),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('fundraisings', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_fundraisings_id'), ['id'], unique=False)

    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_wallet_id', sa.Integer(), nullable=True),
    sa.Column('recipient_wallet_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('deposit', 'withdrawal', 'transfer', name='transaction_type_enum'), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipient_wallet_id'], ['wallets.id'], ),
    sa.ForeignKeyConstraint(['sender_wallet_id'], ['wallets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_entity_relations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.Column('entity_type', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('prefer_help', sa.String(), nullable=True),
    sa.Column('achieves', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('user_spheres',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sphere_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sphere_id'], ['spheres.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'sphere_id')
    )
    op.create_table('user_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('valid_before', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tokens')
    op.drop_table('user_spheres')
    op.drop_table('user_meta')
    op.drop_table('user_entity_relations')
    op.drop_table('transactions')
    with op.batch_alter_table('fundraisings', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_fundraisings_id'))

    op.drop_table('fundraisings')
    with op.batch_alter_table('fundraising_files', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_fundraising_files_id'))

    op.drop_table('fundraising_files')
    op.drop_table('foundation_spheres')
    with op.batch_alter_table('foundation_account_details', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_foundation_account_details_id'))

    op.drop_table('foundation_account_details')
    op.drop_table('company_spheres')
    with op.batch_alter_table('company_account_details', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_company_account_details_id'))

    op.drop_table('company_account_details')
    op.drop_table('admin_tokens')
    op.drop_table('wallets')
    op.drop_table('users')
    with op.batch_alter_table('user_verification_codes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_verification_codes_phone'))
        batch_op.drop_index(batch_op.f('ix_user_verification_codes_id'))

    op.drop_table('user_verification_codes')
    op.drop_table('spheres')
    op.drop_table('news')
    with op.batch_alter_table('foundations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_foundations_id'))

    op.drop_table('foundations')
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_companies_id'))

    op.drop_table('companies')
    op.drop_table('chat_id_list')
    op.drop_table('admins')
    with op.batch_alter_table('admin_verification_codes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_verification_codes_phone'))
        batch_op.drop_index(batch_op.f('ix_admin_verification_codes_id'))

    op.drop_table('admin_verification_codes')
    # ### end Alembic commands ###
