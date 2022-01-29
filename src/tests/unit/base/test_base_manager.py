from base.exceptions import ImproperlyConfigured
from base.manager import BaseManager

import pytest


class SomeClass():
    pass


def test_class_validation():
    with pytest.raises(ImproperlyConfigured):
        BaseManager(SomeClass)


def test_manager_all(manager, user):
    assert manager.all()[0] == user


def test_manager_get(user, manager):
    assert manager.get(pk=user.pk) == user


def test_use_unsuported_fields(user, manager):
    with pytest.raises(ValueError):
        manager.get(wrong_field_name='')


def test_get_with_multiply_fields(manager, user):
    assert manager.get(
        pk=user.pk,
        username=user.username,
        first_name=user.first_name
    ) == user


def test_filter(manager, user):
    assert manager.filter(
        pk=user.pk,
        username=user.username,
        first_name=user.first_name
    )[0] == user


def test_check_fields(mocker, manager, user):
    mocker.patch('base.manager.BaseManager.check_fields')

    manager.get(pk=user.pk)

    manager.check_fields.assert_called_once_with(pk=user.pk)


def test_create(manager):
    manager.create(username='hello', email='world', password='!!!')

    assert manager.exists(username='hello', email='world')


def test_order_by(manager):
    manager.create(
        username='hello',
        email='world',
        password='!!!',
        age=10
    )
    older_one = manager.create(
        username='hello1',
        email='world1',
        password='!!!',
        age=11
    )

    assert older_one == manager.all(order_by='age')[0]
