"""init

Revision ID: 437b0c305f9b
Revises: 
Create Date: 2022-04-11 09:15:32.974614

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from models.ticket import TicketStates
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy_utils.types import EmailType

# revision identifiers, used by Alembic.
revision = '437b0c305f9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', EmailType(), nullable=False),
    sa.Column('state', ChoiceType(choices=TicketStates, impl=sa.Unicode()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', EmailType(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('tickets')
    # ### end Alembic commands ###
