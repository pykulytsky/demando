from tortoise.models import Model
from tortoise import fields


class Event(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=256, unique=True)
    owner = fields.ForeignKeyField('auth.User', related_name='events')


class Question(Model):
    id = fields.IntField(pk=True)

    body = fields.CharField(max_length=1024)
    event = fields.ForeignKeyField('questions.Event')
    author = fields.ForeignKeyField('auth.User', related_name='questions')
    answered = fields.BooleanField(default=False)

    likes = fields.ManyToManyField('auth.User', related_name='liked_questions')


class Poll(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=256)
    owner = fields.ForeignKeyField('auth.User', related_name='polls')


class Option(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=256)
    poll = fields.ForeignKeyField('questions.Poll', related_name='options')


class Vote(Model):
    id = fields.IntField(pk=True)

    poll = fields.ForeignKeyField('questions.Poll', related_name='votes')
    option = fields.ForeignKeyField('questions.Option', related_name='votes')

    owner = fields.ForeignKeyField('auth.User', related_name='votes')
