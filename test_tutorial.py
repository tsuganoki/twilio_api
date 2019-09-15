import pytest
from .make_call import make_call



def test_make_call():
	call = make_call()
	assert call.from_ == "+13126354221"