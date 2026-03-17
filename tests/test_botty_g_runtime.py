import types
from unittest.mock import AsyncMock, Mock

import pytest

import botty_g
from bot import config as bot_config


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


def test_extract_keyword_mentions_counts_variants():
  msg = "Rocket rockets james JAMES's loss losses"
  assert botty_g.extract_keyword_mentions(msg) == {
      "rocket": 2,
      "james": 2,
      "loss": 1,
  }


def test_extract_keyword_mentions_ignores_non_word_matches():
  msg = "rocketeer flotsam glassy"
  assert botty_g.extract_keyword_mentions(msg) == {}


def test_increment_keyword_mentions_persists_counts(monkeypatch):
  set_mock = Mock()
  document_mock = Mock(set=set_mock)
  collection_mock = Mock(document=Mock(return_value=document_mock))
  db_mock = Mock(collection=Mock(return_value=collection_mock))

  monkeypatch.setattr(botty_g, "get_firestore_client", Mock(return_value=db_mock))
  monkeypatch.setattr(botty_g, "_get_firestore_increment", Mock(return_value=lambda n: ("INC", n)))

  botty_g.increment_keyword_mentions("rocket rockets james loss")

  db_mock.collection.assert_called_once_with("stats")
  collection_mock.document.assert_called_once_with("mention_counts")
  set_mock.assert_called_once_with(
      {"rocket": ("INC", 2), "james": ("INC", 1), "loss": ("INC", 1)},
      merge=True,
  )


def test_increment_keyword_mentions_no_matches_skips_firestore(monkeypatch):
  db_mock = Mock()
  monkeypatch.setattr(botty_g, "get_firestore_client", Mock(return_value=db_mock))

  botty_g.increment_keyword_mentions("hello world")

  db_mock.collection.assert_not_called()


def test_get_keyword_mention_count_reads_firestore_value(monkeypatch):
  snapshot_mock = Mock(to_dict=Mock(return_value={"rocket": 9}))
  document_mock = Mock(get=Mock(return_value=snapshot_mock))
  collection_mock = Mock(document=Mock(return_value=document_mock))
  db_mock = Mock(collection=Mock(return_value=collection_mock))
  monkeypatch.setattr(botty_g, "get_firestore_client", Mock(return_value=db_mock))

  count = botty_g.get_keyword_mention_count("rocket")

  assert count == 9


def test_get_keyword_mention_count_defaults_to_zero(monkeypatch):
  snapshot_mock = Mock(to_dict=Mock(return_value=None))
  document_mock = Mock(get=Mock(return_value=snapshot_mock))
  collection_mock = Mock(document=Mock(return_value=document_mock))
  db_mock = Mock(collection=Mock(return_value=collection_mock))
  monkeypatch.setattr(botty_g, "get_firestore_client", Mock(return_value=db_mock))

  assert botty_g.get_keyword_mention_count("rocket") == 0


@pytest.mark.asyncio
async def test_increment_keyword_mentions_async_uses_to_thread(monkeypatch):
  to_thread_mock = AsyncMock(return_value=None)
  monkeypatch.setattr(botty_g.asyncio, "to_thread", to_thread_mock)

  await botty_g.increment_keyword_mentions_async("rocket")

  to_thread_mock.assert_awaited_once_with(
      botty_g.increment_keyword_mentions, "rocket")


@pytest.mark.asyncio
async def test_get_all_keyword_mention_counts_async_uses_to_thread(monkeypatch):
  expected = {"rocket": 1, "james": 2, "loss": 3}
  to_thread_mock = AsyncMock(return_value=expected)
  monkeypatch.setattr(botty_g.asyncio, "to_thread", to_thread_mock)

  result = await botty_g.get_all_keyword_mention_counts_async()

  assert result == expected
  to_thread_mock.assert_awaited_once_with(
      botty_g.get_all_keyword_mention_counts)


@pytest.mark.asyncio
async def test_quote_command_can_select_last_quote(monkeypatch):
  client = botty_g.BottyG()
  client.rocketry = types.SimpleNamespace(
      gen_rocket_command_responses=AsyncMock())
  client.EMOJIS = {}

  monkeypatch.setattr(botty_g.random, "randint", lambda a, b: b)
  monkeypatch.setattr(botty_g, "increment_keyword_mentions", lambda _: None)

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


@pytest.mark.asyncio
async def test_command_messages_skip_counters_and_passive_reactions(monkeypatch):
  client = botty_g.BottyG()
  rocket_mock = AsyncMock()
  reaction_mock = AsyncMock()
  counter_mock = Mock()

  client.rocketry = types.SimpleNamespace(
      gen_rocket_command_responses=rocket_mock)
  client.EMOJIS = {"james": "<james>"}

  monkeypatch.setattr(botty_g.reactions, "add_reactions", reaction_mock)
  monkeypatch.setattr(botty_g, "increment_keyword_mentions", counter_mock)

  message = types.SimpleNamespace(
      content="!rocket",
      author=types.SimpleNamespace(id=1234),
      channel=types.SimpleNamespace(send=AsyncMock()),
      add_reaction=AsyncMock(),
  )

  await client.on_message(message)

  rocket_mock.assert_awaited_once_with(message)
  counter_mock.assert_not_called()
  reaction_mock.assert_not_awaited()


def test_validate_runtime_config_accepts_defaults():
  bot_config.validate_runtime_config()
