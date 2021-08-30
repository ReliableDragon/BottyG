import unittest
import reactions
import asyncio

from unittest.mock import MagicMock
from async_mock import AsyncMock

class TestAddReactions(unittest.TestCase):

  EMOJIS = {
    'bobby_g': "<875428431133810740>",
    'james': "<871742964102205480>",
    'stinky_fish': "<879257588225679390>",
  }

  def setUp(self):
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)

  def tearDown(self):
    self.loop.close()

  def test_reactions(self):
    test_cases = {
      "heyo its your boy bobby g back at it again": "<875428431133810740>",
      "hello it is your gentleman mr. goddard returning to this activity once again": "<875428431133810740>",
      "can we pretend that airplanes in the night sky are actually rockets because those are way cooler": "🚀",
      "i dont know what worcester polytechnic is": "🎓",
      "i dont know what clark university is either": "🎓",
      "you mean worcester like the sauce??": "🏠",
      "ahm frawm bahston massachusetts": "🏠",
      "love your personal space? move to Finland!": "🔭",
      "astronomy: it's the only chance you get to look at things that humans haven't ruined": "🔭",
      "welcome to marsdonalds, the first business on mars, can i take your order?": "🔭",
      "the book war of the worlds is unironically great, i don't have anything sarcastic for it": "📖",
      "go sigma! go alpha! go Sigma Alpha Epsilon!": "🇬🇷",
      "also known as consumption, tuberculosis is what doctors call a right nasty piece of work": "🤒",
      "look up bazooka the cat. you wont regret it.": "🔫",
      "charles lindbergh, famous for flying across the atlantic ocean and also inventing cheese-": "✈️",
      "raid area 51 clap alien cheeks meet at the starbucks in Roswell, NM": "👽",
      "the name esther comes from a jewish woman in the eponymous story of esther, which explains the origins of purim": "💍",
      "the name james was made up by the british so that their kings wouldn't all be named louis like the french": "<871742964102205480>",
      "if someone offers you surstromming it is considered an act of war under international law, and most countries would consider a retalitory strike justified": "<879257588225679390>",
      "father nahum, may i please take the next turn on the butter churn?": "👨‍👦",
    }
    for text, reaction in test_cases.items():
      with self.subTest(msg=text):
        message = AsyncMock()
        message.content = text
        self.loop.run_until_complete(
            reactions.add_reactions(message, self.EMOJIS))
        message.channel.send.assert_not_called()
        message.add_reaction.assert_called_once_with(reaction)
        message.reset_mock()
