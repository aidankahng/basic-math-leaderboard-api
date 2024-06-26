"""Added score keeping

Revision ID: 9f3f74bbf8c3
Revises: 7fa01f00f1b1
Create Date: 2024-04-24 11:51:04.898635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3f74bbf8c3'
down_revision = '7fa01f00f1b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('correct', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('value', sa.Numeric(), nullable=True))

    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quiz_style', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('total_questions', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('score', sa.Numeric(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('points', sa.Numeric(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('points')

    with op.batch_alter_table('quiz', schema=None) as batch_op:
        batch_op.drop_column('score')
        batch_op.drop_column('total_questions')
        batch_op.drop_column('quiz_style')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('value')
        batch_op.drop_column('correct')

    # ### end Alembic commands ###
