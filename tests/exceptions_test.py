import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_to_dict():
    # FyleError instance
    error_message = "This is a test error message"
    status_code = 404
    error = FyleError(status_code=status_code, message=error_message)
    
    error_dict = error.to_dict()
    
    assert error_dict == {'message': error_message}
    assert error.status_code == status_code
