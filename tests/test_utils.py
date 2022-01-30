import pytest
from api.utils import utils


@pytest.mark.parametrize('str_1, exp_1', [
    ('this is a test string', 'This Is A Test String'),
    ('this is also a test string', 'This Is Also A Test String')
])
def test_titlecase(str_1, exp_1):
    assert utils.titlecase(str_1) == exp_1


def test_uppercase():
    assert utils.uppercase('this is a test string') == 'THIS IS A TEST STRING'


def test_convert_phone_number():
    assert utils.convert_phone_number('1234567890') == '(123) 456-7890'
