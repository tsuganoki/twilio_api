import pytest
from .make_call import make_call
from .auth_info import account_phone_number, destination_phone_number



def test_make_call():
	call = make_call(destination_phone_number, account_phone_number)
	assert call.from_ == account_phone_number

