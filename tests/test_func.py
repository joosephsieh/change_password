import pytest
from unittest.mock import patch
from libs.func import validate_password_with_system, validate_password, save_password


@pytest.fixture
def mock_validate_password_with_system_success(request):
    with patch('libs.func.validate_password_with_system', return_value=True):
        yield request


@pytest.fixture
def mock_validate_password_with_system_fail(request):
    with patch('libs.func.validate_password_with_system', return_value=False):
        yield request


@pytest.fixture
def mock_validate_password_scheme_success(request):
    with patch('libs.func.validate_password_scheme', return_value=(True, "It's valid password.")):
        yield request


def test_validate_password_with_system_success():
    result = validate_password_with_system(password="old_password")
    assert result is True


@pytest.mark.usefixtures("mock_validate_password_with_system_fail")
def test_validate_password_with_system_fail():
    result = validate_password(old="old_password", new="new_password")
    assert result == (False, 'Old password should match with system.')


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_success():
    result = validate_password(old="old_password", new="1qaz@WSX3edc$RFV5tgb")
    assert result == (True, "It's valid password.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_too_short():
    result = validate_password(old="old_password", new="1qaz@WSX3e$V5tgb")
    assert result == (False, "At least 18 alphanumeric characters and list of special chars !@#$&*.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_unsupported_char():
    result = validate_password(old="old_password", new="1qaz@WSX3e$V5tgb(){}<>")
    assert result == (False, "At least 18 alphanumeric characters and list of special chars !@#$&*.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_unsupported_doublebyte():
    result = validate_password(old="old_password", new="1qaz@WS測試X3e$V5tgb")
    assert result == (False, "At least 18 alphanumeric characters and list of special chars !@#$&*.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_no_uppercase():
    result = validate_password(old="old_password", new="1qaz@wsx3edc$rf!@#$&*")
    assert result == (False, "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_no_lowercase():
    result = validate_password(old="old_password", new="1QAZ2WSX3EDC4RFV!@#$&*")
    assert result == (False, "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_no_numeric():
    result = validate_password(old="old_password", new="qazwsxedcrfv!@#$&*")
    assert result == (False, "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_no_special_char():
    result = validate_password(old="old_password", new="1qaz2WSX3edc4RFV5tgb")
    assert result == (False, "At least 1 upper case, 1 lower case ,1 numeric, and 1 special character.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_too_many_repeat():
    result = validate_password(old="old_password", new="11qqaazz@@WWSSXX33eeddcc")
    assert result == (False, "No duplicate repeat characters more than 4.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_too_many_special_char():
    result = validate_password(old="old_password", new="!@#$&1qaz2WSX3edc4RFV")
    assert result == (False, "No more than 4 special characters.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success")
def test_validate_password_too_many_number():
    result = validate_password(old="old_password", new="1qaz2@WSX34567890n")
    assert result == (False, "50 % of password should not be a number.")


@pytest.mark.usefixtures("mock_validate_password_with_system_success", "mock_validate_password_scheme_success")
def test_validate_password_too_similar():
    result = validate_password(old="old_password", new="old_password")
    assert result == (False, "Password should not be similar to old password over 80% match.")


def test_save_password():
    result = save_password(password="new_password")
    assert result is True
