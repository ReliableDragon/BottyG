import unittest
import unittest.mock as mock
import asyncio

from unittest.mock import MagicMock
from async_mock import AsyncMock
from rocket_utils import RocketGenerator

class TestRocketGeneration(unittest.TestCase):
  pass

class TestRocketMessageResponses(unittest.TestCase):

  MOCK_EMOJIS = {
    'spotty3': '<spotty3>',
    'spotty4': '<spotty4>',
    'spotty_fire': '<spotty_fire>',
    'spotty_nose_cone': '<spotty_nose_cone>',
    'spotty_nose_cone_rev': '<spotty_nose_cone_rev>',
    'spotty_thruster': '<spotty_thruster>',
    'spotty_thruster_rev': '<spotty_thruster_rev>',
  }

  def setUp(self):
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)

    self.tested = RocketGenerator(self.MOCK_EMOJIS)
    self.tested._get_emoji = MagicMock(side_effect=lambda id: "<" + str(id) + ">")
    self.tested.get_guild = MagicMock()

    self.msg = AsyncMock()

    # self.loop.run_until_complete(self.tested.on_ready())

  def tearDown(self):
    self.loop.close()

  def test_rocket_sends_rocket(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4><spotty3><spotty4><spotty_nose_cone>'
    message = self.msg
    message.content = "!rocket"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_upper_case_rocket_sends_rocket(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4><spotty3><spotty4><spotty_nose_cone>'
    message = self.msg
    message.content = "!ROCKET"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_rooooocket_sends_long_rocket(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4><spotty3><spotty4><spotty3><spotty4><spotty3><spotty4><spotty3><spotty4><spotty3><spotty4><spotty_nose_cone>'
    message = self.msg
    message.content = "!rooooocket"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_roooooocket_sends_rocket_crash(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4>💥  💥<spotty3><spotty4><spotty_nose_cone>'
    message = self.msg
    message.content = "!roooooocket"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_has_calls(
        [mock.call(rocket_msg), mock.call('Oh the humanity!')])
    message.add_reaction.assert_not_called()

  def test_payload_sends_payload(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4>🇦🇺<spotty_nose_cone>'
    message = self.msg
    message.content = "!payload🇦🇺"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_crash_sends_crash(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty3><spotty4><spotty_nose_cone>💥<spotty_nose_cone_rev><spotty4><spotty3><spotty_thruster_rev><spotty_fire>'
    message = self.msg
    message.content = "!crash"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_tekcor_sends_reverse_rocket(self):
    rocket_msg = '\u200b<spotty_nose_cone_rev><spotty4><spotty3><spotty_thruster_rev><spotty_fire>'
    message = self.msg
    message.content = "!tekcor"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_roorckette_sends_wonkyrocket(self):
    rocket_msg = '\u200b<spotty_fire><spotty_thruster><spotty_thruster_rev><spotty_fire><spotty3><spotty4><spotty_nose_cone><spotty_nose_cone_rev>'
    message = self.msg
    message.content = "!roorckette"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_called_once_with(rocket_msg)
    message.add_reaction.assert_not_called()

  def test_roorckkceettero_is_too_long(self):
    message = self.msg
    message.content = "!roorckkcettero"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_not_called()
    message.add_reaction.assert_not_called()

  def test_irrelevant_message_not_replied(self):
    message = self.msg
    message.content = "!not_about_rockets"
    self.loop.run_until_complete(self.tested.gen_rocket_command_responses(message))
    message.channel.send.assert_not_called()
    message.add_reaction.assert_not_called()
