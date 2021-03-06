"""usr create user

Revision ID: b44fc996405a
Revises:
Create Date: 2022-06-16 22:28:41.615733

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b44fc996405a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'usr_users',
        sa.Column(
            'uuid',
            sqlmodel.sql.sqltypes.GUID(),  # noqa
            server_default=sa.text('gen_random_uuid()'),
            nullable=False
        ),
        sa.Column(
            'email',
            sqlmodel.sql.sqltypes.AutoString(),  # noqa
            nullable=False
        ),
        sa.Column(
            'first_name',
            sqlmodel.sql.sqltypes.AutoString(length=127),  # noqa
            nullable=False
        ),
        sa.Column(
            'last_name',
            sqlmodel.sql.sqltypes.AutoString(length=127),  # noqa
            nullable=False
        ),
        sa.Column(
            'date_of_birth',
            sa.Date(),
            nullable=True
        ),
        sa.Column(
            'gender',
            postgresql.ENUM('male', 'female', name='usr_gender'),
            nullable=True
        ),
        sa.Column(
            'email_verified',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False
        ),
        sa.Column(
            'is_superuser',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False
        ),
        sa.Column(
            'is_staff',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False
        ),
        sa.Column(
            'is_deleted',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('current_timestamp(0)'),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('current_timestamp(0)'),
            nullable=False
        ),
        sa.Column(
            'hashed_password',
            sqlmodel.sql.sqltypes.AutoString(),  # noqa
            nullable=False
        ),
        sa.PrimaryKeyConstraint(
            'uuid',
            name=op.f('pk_usr_users')
        )
    )

    op.create_index(
        op.f('ix_usr_users_email'),
        'usr_users',
        ['email'],
        unique=True
    )
    op.create_index(
        op.f('ix_usr_users_first_name'),
        'usr_users',
        ['first_name'],
        unique=False
    )
    op.create_index(
        op.f('ix_usr_users_last_name'),
        'usr_users',
        ['last_name'],
        unique=False
    )
    op.create_index(
        op.f('ix_usr_users_uuid'),
        'usr_users',
        ['uuid'],
        unique=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usr_users_uuid'), table_name='usr_users')
    op.drop_index(op.f('ix_usr_users_last_name'), table_name='usr_users')
    op.drop_index(op.f('ix_usr_users_first_name'), table_name='usr_users')
    op.drop_index(op.f('ix_usr_users_email'), table_name='usr_users')
    op.drop_table('usr_users')
    # ### end Alembic commands ###
    op.execute("drop type usr_gender;")
