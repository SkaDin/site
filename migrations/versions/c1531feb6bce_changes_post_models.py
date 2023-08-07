"""changes Post models

Revision ID: c1531feb6bce
Revises: e946e0a4e7da
Create Date: 2023-08-07 01:10:49.778090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1531feb6bce'
down_revision = 'e946e0a4e7da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=124),
               type_=sa.String(length=17),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('active')
        batch_op.drop_column('uniquifier_constraint')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uniquifier_constraint', sa.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('active', sa.BOOLEAN(), nullable=True))

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=17),
               type_=sa.VARCHAR(length=124),
               existing_nullable=False)

    # ### end Alembic commands ###
