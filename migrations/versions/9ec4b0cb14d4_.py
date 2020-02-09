"""empty message

Revision ID: 9ec4b0cb14d4
Revises: 410521e43cf3
Create Date: 2020-02-08 22:35:17.004164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ec4b0cb14d4'
down_revision = '410521e43cf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=50), nullable=False),
    sa.Column('descripcion', sa.String(length=50), nullable=False),
    sa.Column('fecha_limite', sa.String(length=50), nullable=False),
    sa.Column('estado_evento', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requerimiento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('descripcion', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requerimiento')
    op.drop_table('evento')
    # ### end Alembic commands ###