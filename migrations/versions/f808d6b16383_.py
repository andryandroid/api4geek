"""empty message

Revision ID: f808d6b16383
Revises: 6a7f9f4b071c
Create Date: 2020-02-10 16:34:11.635683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f808d6b16383'
down_revision = '6a7f9f4b071c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('evento_requerimiento',
    sa.Column('evento_id', sa.Integer(), nullable=False),
    sa.Column('requerimiento_id', sa.Integer(), nullable=False),
    sa.Column('cantidad_requerida', sa.Integer(), nullable=False),
    sa.Column('cantidad_actual', sa.Integer(), nullable=False),
    sa.Column('estado_requerimiento', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['evento_id'], ['evento.id'], ),
    sa.ForeignKeyConstraint(['requerimiento_id'], ['requerimiento.id'], ),
    sa.PrimaryKeyConstraint('evento_id', 'requerimiento_id')
    )
    op.create_foreign_key(None, 'evento', 'usuario', ['usuario_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'evento', type_='foreignkey')
    op.drop_table('evento_requerimiento')
    # ### end Alembic commands ###