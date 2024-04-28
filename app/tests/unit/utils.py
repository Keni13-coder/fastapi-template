async def assertional_session_aexit(fakeUOW):
    assert fakeUOW.session.is_close
    assert fakeUOW.session.is_rollback
