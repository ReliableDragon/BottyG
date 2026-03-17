import types
from unittest import mock
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

import botty_g


class MockUser:
  def __init__(self, name, user_id):
    self.name = name
    self.id = user_id

  def __eq__(self, other):
    return self.name == other.name and self.id == other.id


@pytest_asyncio.fixture
async def ready_bot():
  own_user = MockUser(name="Jean Valjean", user_id=24601)
  with mock.patch(
      "botty_g.BottyG.user",
      new=mock.PropertyMock(return_value=own_user)):
    tested = botty_g.BottyG()
    tested._get_emoji = mock.MagicMock(side_effect=lambda emoji_id: f"<{emoji_id}>")
    tested.get_guild = mock.MagicMock(side_effect=lambda guild_id: f"[{guild_id}]")
    await tested.on_ready()
    yield tested, own_user


@pytest.fixture
def message_factory():
  def _make(content, author=None):
    return types.SimpleNamespace(
        content=content,
        author=author or MockUser(name="Javert", user_id=911),
        channel=types.SimpleNamespace(send=AsyncMock()),
        add_reaction=AsyncMock(),
    )

  return _make


def test_atomic_frontier_set_up_properly(ready_bot):
  tested, _ = ready_bot
  assert tested.atomic_frontier == "[800703973890850836]"


def test_demo_server_set_up_properly(ready_bot):
  tested, _ = ready_bot
  assert tested.demo_server == "[879111900485517394]"


@pytest.mark.asyncio
async def test_no_response_to_own_message(ready_bot, message_factory):
  tested, own_user = ready_bot
  message = message_factory("!rocket", author=own_user)

  await tested.on_message(message)

  message.channel.send.assert_not_called()
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
async def test_quote_sends_quote(ready_bot, message_factory, monkeypatch):
  tested, _ = ready_bot
  message = message_factory("!quote")
  monkeypatch.setattr(botty_g.random, "randint", lambda a, b: 0)

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(botty_g.QUOTES[0])
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
async def test_advice_alias_sends_quote(ready_bot, message_factory, monkeypatch):
  tested, _ = ready_bot
  message = message_factory("!advice")
  monkeypatch.setattr(botty_g.random, "randint", lambda a, b: len(botty_g.QUOTES) - 1)

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(botty_g.QUOTES[-1])
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, expected",
    sorted(botty_g.REACTION_IMAGES.items()),
)
async def test_reaction_image_commands(ready_bot, message_factory, command, expected):
  tested, _ = ready_bot
  message = message_factory(command)

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(expected)
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, expected",
    [
      ("!help", botty_g.COMMANDS),
      ("!commands", botty_g.COMMANDS),
      ("!reactions", botty_g.REACTION_IMAGES_MSG),
    ],
)
async def test_help_and_reaction_list_commands(ready_bot, message_factory, command, expected):
  tested, _ = ready_bot
  message = message_factory(command)

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(expected)
  message.add_reaction.assert_not_called()


def test_reaction_images_in_sync_with_reaction_images_msg():
  gif_list = sorted(botty_g.REACTION_IMAGES.keys())
  reactions_list = sorted(botty_g.REACTION_IMAGES_MSG[3:-3].strip().split("\n"))
  assert gif_list == reactions_list


@pytest.mark.asyncio
async def test_time_zone_response(ready_bot, message_factory):
  tested, _ = ready_bot
  message = message_factory("!convert PDT 23:59 EST GMT CET")
  expected = (
      "23:59 PDT is:\n"
      "  01:59 EST\n"
      "  06:59 GMT\n"
      "  07:59 CET"
  )

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(expected)
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
async def test_roorckette_sends_wonkyrocket(ready_bot, message_factory):
  tested, _ = ready_bot
  message = message_factory("!roorckette")
  expected = (
      "\u200b<871843033883213914><871842514213142598>"
      "<875529093729357855><871843033883213914><868858496257515520>"
      "<868858506776817675><868858516687958126><875529103984431154>"
  )

  await tested.on_message(message)

  message.channel.send.assert_called_once_with(expected)
  message.add_reaction.assert_not_called()


@pytest.mark.asyncio
async def test_reaction_trigger(ready_bot, message_factory):
  tested, _ = ready_bot
  message = message_factory("heyo its your boy bobby g back at it again")

  await tested.on_message(message)

  message.channel.send.assert_not_called()
  message.add_reaction.assert_called_once_with("<875428431133810740>")


@pytest.mark.asyncio
async def test_multi_reaction_trigger(ready_bot, message_factory):
  tested, _ = ready_bot
  message = message_factory("heyo its your boy bobby g back at it again with the space planes")

  await tested.on_message(message)

  message.channel.send.assert_not_called()
  message.add_reaction.assert_has_calls(
      [mock.call("<875428431133810740>"), mock.call("🔭")])
