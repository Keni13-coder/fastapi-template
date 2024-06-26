"""init

Revision ID: cc077ac89679
Revises: 
Create Date: 2024-05-06 16:33:16.964308

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc077ac89679"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("is_authenticated", sa.Boolean(), nullable=False),
        sa.Column(
            "role", sa.Enum("super_user", "user", name="userrole"), nullable=False
        ),
        sa.Column("password", sa.String(length=80), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        sa.UniqueConstraint("login", name=op.f("user_login_key")),
    )
    op.create_index(op.f("user_id_idx"), "user", ["id"], unique=False)
    op.create_table(
        "token",
        sa.Column("jti", sa.UUID(), nullable=False),
        sa.Column("user_uid", sa.UUID(), nullable=False),
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("access_iat", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_uid"],
            ["user.id"],
            name=op.f("token_user_uid_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("token_pkey")),
        sa.UniqueConstraint("device_id", name=op.f("token_device_id_key")),
    )
    op.create_index(op.f("token_id_idx"), "token", ["id"], unique=False)
    op.create_index(op.f("token_user_uid_idx"), "token", ["user_uid"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("token_user_uid_idx"), table_name="token")
    op.drop_index(op.f("token_id_idx"), table_name="token")
    op.drop_table("token")
    op.drop_index(op.f("user_id_idx"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
