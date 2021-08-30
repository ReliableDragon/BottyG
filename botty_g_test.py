import unittest
import unittest.mock as mock
import botty_g
import asyncio
import logging

from logging.handlers import RotatingFileHandler
from unittest.mock import MagicMock
from botty_g import BottyG
from async_mock import AsyncMock

my_handler = RotatingFileHandler(
    'botty_g_test.log', mode='a', maxBytes=5*1024*1024, backupCount=2)
my_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)


class MockUser:

  def __init__(self, name, id):
    self.name = name
    self.id = id

  def __eq__(self, other):
    return self.name == other.name and self.id == other.id

  def __ne__(self, other):
    return not self.__eq__(other)

# These overlap with rocket_utils_test, but are kept here because the
# integration with the _get_emoji() method is critical.
class TestEmojiLoading(unittest.TestCase):

  def setUp(self):
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)

    self.patcher = mock.patch(
        "botty_g.BottyG.user", new=mock.PropertyMock())
    self.mock_user = self.patcher.start()

    self.tested = BottyG()
    self.tested._get_emoji = MagicMock(side_effect=lambda id: "<" + str(id) + ">")
    self.tested.get_guild = MagicMock()

    self.loop.run_until_complete(self.tested.on_ready())

  def tearDown(self):
    self.patcher.stop()
    self.loop.close()

  def test_rocket(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET,
        "<871843033883213914><871842514213142598><868858496257515520><868858506776817675><868858516687958126>")

  def test_rocket_rev(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_REV,
        "<875529103984431154><868858506776817675><868858496257515520><875529093729357855><871843033883213914>")

  def test_rocket_nose(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_NOSE,
        "<868858516687958126>")

  def test_rocket_nose_rev(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_NOSE_REV,
        "<875529103984431154>")

  def test_rocket_thrust(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_THRUST,
        "<871843033883213914><871842514213142598>")

  def test_rocket_thrust_rev(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_THRUST_REV,
        "<875529093729357855><871843033883213914>")

  def test_rocket_body(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_BODY,
        "<868858496257515520><868858506776817675>")

  def test_rocket_body_rev(self):
    self.assertEqual(
        self.tested.rocketry.ROCKET_BODY_REV,
        "<868858506776817675><868858496257515520>")


class TestMessageResponses(unittest.TestCase):

  def setUp(self):
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)

    user = MockUser(name='Jean Valjean', id=24601)
    self.patcher = mock.patch(
        "botty_g.BottyG.user",
        new=mock.PropertyMock(return_value = user))
    self.mock_user = self.patcher.start()

    self.tested = BottyG()
    self.tested._get_emoji = MagicMock(side_effect=lambda id: "<" + str(id) + ">")
    self.tested.get_guild = MagicMock()

    self.msg = AsyncMock()
    # We have to provide an author, or else the value stored here is an
    # AsyncMock, which when =='ed with the MockUser provided by the patch above
    # will result in a coroutine, which for some reason evaluates to true,
    # and prevents any calls from passing the check against self-messages.
    self.msg.author = MockUser(name='Javert', id=911)

    self.loop.run_until_complete(self.tested.on_ready())

  def tearDown(self):
    self.patcher.stop()
    self.loop.close()

  def test_no_response_to_own_message(self):
    message = AsyncMock()
    message.content = "!rocket"
    message.author = MockUser(name='Jean Valjean', id=24601)
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_not_called()
    message.add_reaction.assert_not_called()

  def test_quote_sends_quote(self):
    rocket_msg = "It is difficult to say what is impossible, for the dream of yesterday is the hope of today and the reality of tomorrow."
    message = self.msg
    message.content = "!quote"
    with mock.patch('random.randint', new=lambda a, b: 0):
      self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  # Already tested in rocket_utils_test, kept here for integration testing.
  def test_roorckette_sends_wonkyrocket(self):
    rocket_msg = "\u200b<871843033883213914><871842514213142598><875529093729357855><871843033883213914><868858496257515520><868858506776817675><868858516687958126><875529103984431154>"
    message = self.msg
    message.content = "!roorckette"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_baguette_sends_clip(self):
    rocket_msg = "https://cdn.discordapp.com/attachments/875464533362216960/880994913918013500/this_baguette.mp4"
    message = self.msg
    message.content = "!baguette"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_snacktime_sends_clip(self):
    rocket_msg = "https://cdn.discordapp.com/attachments/800703974205685790/820105727707447336/sandful_of_hand.mp4"
    message = self.msg
    message.content = "!snacktime"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_danceparty_sends_clip(self):
    rocket_msg = "https://cdn.discordapp.com/attachments/800703974205685790/830025367325900800/Go-James-Go.gif"
    message = self.msg
    message.content = "!danceparty"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_nope_sends_clip(self):
    rocket_msg = "https://tenor.com/view/simpsons-bart-simpson-grampa-simpson-old-man-hi-bye-gif-8390063"
    message = self.msg
    message.content = "!nope"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_synapsid_sends_clip(self):
    rocket_msg = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Leonid_Brezhnev_and_Richard_Nixon_talks_in_1973.png/1600px-Leonid_Brezhnev_and_Richard_Nixon_talks_in_1973.png"
    message = self.msg
    message.content = "!synapsid"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_timezones_sends_clip(self):
    rocket_msg = "https://tenor.com/view/time-zones-wp-fairly-oddparents-gif-21690567"
    message = self.msg
    message.content = "!timezones"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_confusion_sends_clip(self):
    rocket_msg = "https://tenor.com/view/umm-confused-blinking-okay-white-guy-blinking-gif-7513882"
    message = self.msg
    message.content = "!confusion"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_perfect_sends_clip(self):
    rocket_msg = "https://tenor.com/view/pacha-perfect-emperors-new-groove-very-good-gif-5346522"
    message = self.msg
    message.content = "!perfection"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_cow_sends_clip(self):
    rocket_msg = "https://tenor.com/view/cow-airflow-diagram-vectors-aerodynamics-gif-4785226"
    message = self.msg
    message.content = "!cow"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_clap_sends_clip(self):
    rocket_msg = "https://tenor.com/view/good-job-clapping-leonardo-dicaprio-bravo-great-gif-7248435"
    message = self.msg
    message.content = "!clap"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_help_sends_help(self):
    commands_msg = botty_g.COMMANDS
    message = self.msg
    message.content = "!help"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(commands_msg)
    message.add_reaction.assert_not_called()

  def test_reactions_sends_reactions(self):
    commands_msg = botty_g.REACTION_IMAGES_MSG
    message = self.msg
    message.content = "!reactions"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(commands_msg)
    message.add_reaction.assert_not_called()

  def test_reaction_images_in_sync_with_reaction_images_msg(self):
    gif_list = sorted(botty_g.REACTION_IMAGES.keys())
    reactions_list = sorted(botty_g.REACTION_IMAGES_MSG[3:-3].strip().split('\n'))
    self.assertListEqual(gif_list, reactions_list)

  def test_time_zone_response(self):
    time_zone_message = ("23:59 PDT is:\n"
          "  01:59 EST\n"
          "  06:59 GMT\n"
          "  07:59 CET")
    message = self.msg
    message.content = "!convert PDT 23:59 EST GMT CET"
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_called_once_with(time_zone_message)
    message.add_reaction.assert_not_called()

  # Already tested in reaction_test, kept here for integration purposes.
  def test_reaction(self):
    text = "heyo its your boy bobby g back at it again"
    reaction = "<875428431133810740>"
    message = self.msg
    message.content = text
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_not_called()
    message.add_reaction.assert_called_once_with(reaction)
    message.reset_mock()

  # Already tested in reaction_test, kept here for integration purposes.
  def test_multi_reaction(self):
    text = "heyo its your boy bobby g back at it again with the space planes"
    bobby_g_reaction = "<875428431133810740>"
    space_reaction = "🔭"
    message = self.msg
    message.content = text
    self.loop.run_until_complete(self.tested.on_message(message))
    message.channel.send.assert_not_called()
    message.add_reaction.assert_has_calls(
        [mock.call(bobby_g_reaction), mock.call(space_reaction)])


if __name__ == '__main__':
  unittest.main()
