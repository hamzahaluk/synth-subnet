"""add table for miner rewards

Revision ID: 1154ae96bd0a
Revises: 9f5c6d18896d
Create Date: 2024-12-08 15:49:07.612838

This migration introduces the `miner_rewards` table to store data
about rewards associated with miners. Each entry includes details
about validation times, reward periods, and metadata.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "1154ae96bd0a"
down_revision: Union[str, None] = "9f5c6d18896d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the `miner_rewards` table
    op.create_table(
        "miner_rewards",
        sa.Column("id", sa.BigInteger, primary_key=True, nullable=False),
        sa.Column("miner_uid", sa.Integer, nullable=False, comment="Unique identifier for the miner"),
        sa.Column(
            "validation_time", 
            sa.TIMESTAMP(timezone=True), 
            nullable=False, 
            comment="Timestamp when the reward was validated"
        ),
        sa.Column(
            "start_time", 
            sa.TIMESTAMP(timezone=True), 
            nullable=False, 
            comment="Start time of the reward period"
        ),
        sa.Column(
            "reward_details", 
            JSONB, 
            nullable=False, 
            comment="Additional details of the reward in JSON format"
        ),
    )
    # Add indexes for faster query performance
    op.create_index(
        "ix_miner_rewards_validation_time",
        "miner_rewards",
        ["validation_time"],
    )
    op.create_index(
        "ix_miner_rewards_miner_uid", 
        "miner_rewards", 
        ["miner_uid"]
    )


def downgrade() -> None:
    # Drop indexes first to avoid dependency issues
    op.drop_index(
        "ix_miner_rewards_validation_time", 
        table_name="miner_rewards"
    )
    op.drop_index(
        "ix_miner_rewards_miner_uid", 
        table_name="miner_rewards"
    )
    # Drop the `miner_rewards` table
    op.drop_table("miner_rewards")
