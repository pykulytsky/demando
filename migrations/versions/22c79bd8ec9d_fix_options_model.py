"""fix options model

Revision ID: 22c79bd8ec9d
Revises: dcee17a6aa3c
Create Date: 2021-04-05 22:50:35.809886

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '22c79bd8ec9d'
down_revision = 'dcee17a6aa3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_votes_pk', table_name='votes')
    op.drop_table('votes')


    op.drop_table('likes')

    op.drop_index('ix_questions_pk', table_name='questions')
    op.drop_table('questions')
    op.drop_index('ix_events_pk', table_name='events')
    op.drop_table('events')
    op.drop_index('ix_options_pk', table_name='options')
    op.drop_table('options')

    op.drop_index('ix_polls_pk', table_name='polls')
    op.drop_table('polls')
    op.drop_index('ix_users_pk', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_roles_pk', table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('pk', sa.INTEGER(), server_default=sa.text("nextval('roles_pk_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('verbose', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('pk', name='roles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_roles_pk', 'roles', ['pk'], unique=False)
    op.create_table('votes',
    sa.Column('pk', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('poll_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('owner_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('option_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['option_pk'], ['options.pk'], name='votes_option_pk_fkey'),
    sa.ForeignKeyConstraint(['owner_pk'], ['users.pk'], name='votes_owner_pk_fkey'),
    sa.ForeignKeyConstraint(['poll_pk'], ['polls.pk'], name='votes_poll_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='votes_pkey')
    )
    op.create_index('ix_votes_pk', 'votes', ['pk'], unique=False)
    op.create_table('likes',
    sa.Column('user_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('question_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['question_pk'], ['questions.pk'], name='likes_question_pk_fkey'),
    sa.ForeignKeyConstraint(['user_pk'], ['users.pk'], name='likes_user_pk_fkey')
    )
    op.create_table('events',
    sa.Column('pk', sa.INTEGER(), server_default=sa.text("nextval('events_pk_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_pk'], ['users.pk'], name='events_owner_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='events_pkey'),
    sa.UniqueConstraint('name', name='events_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_events_pk', 'events', ['pk'], unique=False)
    op.create_table('questions',
    sa.Column('pk', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('event_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('author_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('answered', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('likes_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_pk'], ['users.pk'], name='questions_author_pk_fkey'),
    sa.ForeignKeyConstraint(['event_pk'], ['events.pk'], name='questions_event_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='questions_pkey')
    )
    op.create_index('ix_questions_pk', 'questions', ['pk'], unique=False)
    op.create_table('options',
    sa.Column('pk', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('poll_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['poll_pk'], ['polls.pk'], name='options_poll_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='options_pkey')
    )
    op.create_index('ix_options_pk', 'options', ['pk'], unique=False)
    op.create_table('polls',
    sa.Column('pk', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('owner_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_pk'], ['users.pk'], name='polls_owner_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='polls_pkey')
    )
    op.create_index('ix_polls_pk', 'polls', ['pk'], unique=False)
    op.create_table('users',
    sa.Column('pk', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('role_pk', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('verification_code', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_pk'], ['roles.pk'], name='users_role_pk_fkey'),
    sa.PrimaryKeyConstraint('pk', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.create_index('ix_users_pk', 'users', ['pk'], unique=False)
    # ### end Alembic commands ###
