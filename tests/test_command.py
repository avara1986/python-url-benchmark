import pytest

from ub.url_benchmark import Command


class AsyncMock:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *error_info):
        return self

    async def text(self):
        return '{"my": "json"}'


def mock_client_get_ok(self, *args, **kwargs):
    mock_response = AsyncMock()
    mock_response.status = 200
    return mock_response


def mock_client_get_error(self, *args, **kwargs):
    mock_response = AsyncMock()
    mock_response.status = 500
    return mock_response


def test_base_error():
    arguments = ["http://localhost:0000000", "2"]
    cmd = Command(arguments=arguments, autorun=False)
    result = cmd.run()
    assert result is True


@pytest.mark.asyncio
async def test_call_url_ok(monkeypatch):
    monkeypatch.setattr('aiohttp.ClientSession.get', mock_client_get_ok)

    arguments = ["http://localhost", "2"]
    cmd = Command(arguments=arguments, autorun=False)
    result = await cmd.call_url("http://localhost", {}, 0)
    assert result == '{"my": "json"}'


@pytest.mark.asyncio
async def test_call_url_error(monkeypatch):
    monkeypatch.setattr('aiohttp.ClientSession.get', mock_client_get_error)

    arguments = ["http://localhost", "2"]
    cmd = Command(arguments=arguments, autorun=False)
    result = await cmd.call_url("http://localhost", {}, 0)
    assert result is False
