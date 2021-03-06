"""grvscdqgr

Revision ID: fbbe95e38d47
Revises: df73d74b3946
Create Date: 2022-02-22 21:52:18.879845

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fbbe95e38d47'
down_revision = 'df73d74b3946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_cart',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['Cart.Id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['Products.ProductID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Id')
    )
    op.add_column('Cart', sa.Column('UserID', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Cart', 'users', ['UserID'], ['id'])
    op.drop_constraint('users_ibfk_1', 'users', type_='foreignkey')
    op.drop_column('users', 'CartId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('CartId', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_ibfk_1', 'users', 'Cart', ['CartId'], ['Id'])
    op.drop_constraint(None, 'Cart', type_='foreignkey')
    op.drop_column('Cart', 'UserID')
    op.drop_table('product_cart')
    # ### end Alembic commands ###
