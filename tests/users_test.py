import pytest
from core import db
from core.models.users import User

@pytest.fixture(scope='function')
def existing_user():
    return User.query.first()


def test_user_repr(existing_user):
    """Test the __repr__ method of the User model"""
    user = existing_user
    assert repr(user) == '<User %r>' % user.username


def test_user_filter(existing_user):
    """Test the filter method of the User model"""
    user = existing_user
    filtered_users = User.filter(User.username == user.username).all()
    assert filtered_users[0].username == user.username


def test_get_by_id(existing_user):
    """Test the get_by_id method of the User model"""
    user = existing_user
    retrieved_user = User.get_by_id(user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id


def test_get_by_email(existing_user):
    """Test the get_by_email method of the User model"""
    user = existing_user
    retrieved_user = User.get_by_email(user.email)
    assert retrieved_user is not None
    assert retrieved_user.email == user.email
