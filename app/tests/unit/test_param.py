import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture(scope="module")
def id_fix():
    return 14


@pytest.fixture(scope="module")
def data(id_fix):
    return {"id": id_fix}


@pytest.fixture(scope="module")
async def on_start(request: SubRequest):
    your_fixture = request.getfixturevalue(request.param)

    print(your_fixture)
    return your_fixture


@pytest.mark.parametrize("on_start", ["data"], indirect=["on_start"])
@pytest.mark.usefixtures("on_start")
class TestParamStart:
    async def test_params(self, on_start):
        # assert await on_start()
        # assert isinstance(on_start, dict)
        print(type(on_start))

    async def test_two_params(self, on_start):
        on_start["id"]
        print(type(on_start))
