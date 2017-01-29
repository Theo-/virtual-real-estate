"""empty message

Revision ID: 44d9aadaf9ec
Revises: 
Create Date: 2017-01-28 19:44:46.262712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44d9aadaf9ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'classifiers_ibfk_1', 'classifiers', type_='foreignkey')
    op.drop_constraint(u'listing_mapped_images_ibfk_1', 'listing_mapped_images', type_='foreignkey')
    op.drop_constraint(u'listing_mapped_images_ibfk_2', 'listing_mapped_images', type_='foreignkey')
    op.drop_constraint(u'user_visited_listings_ibfk_1', 'user_visited_listings', type_='foreignkey')
    op.drop_constraint(u'user_visited_listings_ibfk_2', 'user_visited_listings', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(u'user_visited_listings_ibfk_2', 'user_visited_listings', 'users', ['user_id'], ['id'])
    op.create_foreign_key(u'user_visited_listings_ibfk_1', 'user_visited_listings', 'listing', ['listing'], ['id'])
    op.create_foreign_key(u'listing_mapped_images_ibfk_2', 'listing_mapped_images', 'listing_image', ['listing_image'], ['id'])
    op.create_foreign_key(u'listing_mapped_images_ibfk_1', 'listing_mapped_images', 'listing', ['listing'], ['id'])
    op.create_foreign_key(u'classifiers_ibfk_1', 'classifiers', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
