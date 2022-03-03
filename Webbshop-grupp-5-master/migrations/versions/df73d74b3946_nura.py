"""nura

Revision ID: df73d74b3946
Revises: 
Create Date: 2022-02-22 21:42:32.281133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df73d74b3946'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cart',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Categories',
    sa.Column('CategoryID', sa.Integer(), nullable=False),
    sa.Column('CategoryName', sa.String(length=80), nullable=False),
    sa.Column('Description', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('CategoryID')
    )
    op.create_table('MailAdresser',
    sa.Column('EpostID', sa.Integer(), nullable=False),
    sa.Column('Epostadress', sa.String(length=40), nullable=False),
    sa.Column('IsActive', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('EpostID'),
    sa.UniqueConstraint('Epostadress')
    )
    op.create_table('Newsletter',
    sa.Column('NewsletterId', sa.Integer(), nullable=False),
    sa.Column('Title', sa.String(length=40), nullable=False),
    sa.Column('Content', sa.String(length=1000), nullable=False),
    sa.Column('HasBeenSent', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('NewsletterId')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Products',
    sa.Column('ProductID', sa.Integer(), nullable=False),
    sa.Column('ProductName', sa.String(length=40), nullable=False),
    sa.Column('SupplierID', sa.Integer(), nullable=False),
    sa.Column('CategoryId', sa.Integer(), nullable=False),
    sa.Column('QuantityPerUnit', sa.String(length=20), nullable=False),
    sa.Column('UnitPrice', sa.Float(), nullable=False),
    sa.Column('UnitsInStock', sa.Integer(), nullable=False),
    sa.Column('UnitsOnOrder', sa.Integer(), nullable=False),
    sa.Column('ReorderLevel', sa.Integer(), nullable=False),
    sa.Column('Discontinued', sa.Boolean(), nullable=False),
    sa.Column('CampaignPrice', sa.Integer(), nullable=False),
    sa.Column('Rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['CategoryId'], ['Categories.CategoryID'], ),
    sa.PrimaryKeyConstraint('ProductID')
    )
    op.create_table('newsletter_mails',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Mail_id', sa.Integer(), nullable=True),
    sa.Column('Newsletter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Mail_id'], ['MailAdresser.EpostID'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['Newsletter_id'], ['Newsletter.NewsletterId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('first_name', sa.String(length=100), server_default='', nullable=False),
    sa.Column('last_name', sa.String(length=100), server_default='', nullable=False),
    sa.Column('CartId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['CartId'], ['Cart.Id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('ProductRating',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Product_id', sa.Integer(), nullable=True),
    sa.Column('Point_1', sa.Integer(), nullable=False),
    sa.Column('Point_2', sa.Integer(), nullable=False),
    sa.Column('Point_3', sa.Integer(), nullable=False),
    sa.Column('Point_4', sa.Integer(), nullable=False),
    sa.Column('Point_5', sa.Integer(), nullable=False),
    sa.Column('Point_total', sa.Integer(), nullable=False),
    sa.Column('Point_count', sa.Integer(), nullable=False),
    sa.Column('Point_avarage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['Product_id'], ['Products.ProductID'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('ProductRating')
    op.drop_table('users')
    op.drop_table('newsletter_mails')
    op.drop_table('Products')
    op.drop_table('roles')
    op.drop_table('Newsletter')
    op.drop_table('MailAdresser')
    op.drop_table('Categories')
    op.drop_table('Cart')
    # ### end Alembic commands ###