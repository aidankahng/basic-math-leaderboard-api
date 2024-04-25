"""made more quiz params non-null

Revision ID: e9af7c7fcbf6
Revises: 0c595f2e9f22
Create Date: 2024-04-24 19:09:55.666605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9af7c7fcbf6'
down_revision = '0c595f2e9f22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.alter_column('total_questions',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('total_correct',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('total_attempted',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('score',
               existing_type=sa.NUMERIC(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.alter_column('score',
               existing_type=sa.NUMERIC(),
               nullable=True)
        batch_op.alter_column('total_attempted',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('total_correct',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('total_questions',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###