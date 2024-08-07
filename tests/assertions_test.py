import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

def test_assert_auth_raises_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False, 'UNAUTHORIZED')
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == 'UNAUTHORIZED'

def test_assert_true_raises_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        assert_true(False, 'FORBIDDEN')
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == 'FORBIDDEN'

def test_assert_valid_raises_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        assert_valid(False, 'BAD REQUEST')
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == 'BAD REQUEST'

def test_assert_found_raises_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        assert_found(None, 'NOT FOUND')
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == 'NOT FOUND'
