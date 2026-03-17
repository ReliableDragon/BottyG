import types
from unittest.mock import AsyncMock, Mock

import pytest

import botty_g


def _mock_secret_response(token):
  return types.SimpleNamespace(
      payload=types.SimpleNamespace(data=token.encode("utf-8")))


def test_bottyg_initializes_discord_client_state():
  client = botty_g.BottyG()
  assert hasattr(client, "http")
  assert client.intents.message_content is True


def test_get_discord_token_success(monkeypatch):
  mock_client = Mock()
  mock_client.access_secret_version.return_value = _mock_secret_response(
      "token-123")
  mock_ctor = Mock(return_value=mock_client)
  monkeypatch.setattr(
      botty_g.secretmanager, "SecretManagerServiceClient", mock_ctor)

  token = botty_g.get_discord_token()

  assert token == "token-123"
  mock_client.access_secret_version.assert_called_once_with(
      request={"name": "projects/bottyg/secrets/discord_bot_token/versions/latest"})


def test_get_discord_token_empty_raises(monkeypatch):
  mock_client = Mock()
  mock_client.access_secret_version.return_value = _mock_secret_response(" ")
  monkeypatch.setattr(
      botty_g.secretmanager, "SecretManagerServiceClient", Mock(return_value=mock_client))

  with pytest.raises(ValueError, match="is empty"):
    botty_g.get_discord_token()


def test_get_discord_token_propagates_secret_manager_errors(monkeypatch):
  mock_client = Mock()
  mock_client.access_secret_version.side_effect = RuntimeError("boom")
  monkeypatch.setattr(
      botty_g.secretmanager, "SecretManagerServiceClient", Mock(return_value=mock_client))

  with pytest.raises(RuntimeError, match="boom"):
    botty_g.get_discord_token()


@pytest.mark.asyncio
async def test_quote_command_can_select_last_quote(monkeypatch):
  client = botty_g.BottyG()
  client.rocketry = types.SimpleNamespace(
      gen_rocket_command_responses=AsyncMock())
  client.EMOJIS = {}

  monkeypatch.setattr(botty_g.random, "randint", lambda a, b: b)

  message = types.SimpleNamespace(
      content="!quote",
      author=types.SimpleNamespace(id=1234),
      channel=types.SimpleNamespace(send=AsyncMock()),
      add_reaction=AsyncMock(),
  )

  await client.on_message(message)

  message.channel.send.assert_called()
  sent_msg = message.channel.send.call_args[0][0]
  assert sent_msg == botty_g.QUOTES[-1]
