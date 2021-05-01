import pytest

from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(
        email="normal@user.com",
        first_name="test",
        last_name="user",
        password="foo",
    )
    assert user.email == "normal@user.com"
    assert user.first_name == "test"
    assert user.last_name == "user"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert str(user) == "normal@user.com"
    # username is None for the AbstractUser option
    assert user.username is None
    with pytest.raises(TypeError):
        User.objects.create_user()
    with pytest.raises(TypeError):
        User.objects.create_user(email="")
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="foo")


def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser("super@user.com", "foo")
    assert admin_user.email == "super@user.com"
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True
    assert str(admin_user) == "super@user.com"
    # username is None for the AbstractUser option
    assert admin_user.username is None
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="super@user.com", password="foo", is_superuser=False
        )
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="super@user.com", password="foo", is_staff=False
        )