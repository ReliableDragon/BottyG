import unittest
import reactions
import asyncio

from unittest.mock import MagicMock
from unittest.mock import Mock
from async_mock import AsyncMock

class MockUser:
  def __init__(self, id):
    self.id = id

class TestAddReactions(unittest.TestCase):

  EMOJIS = {
    'bobby_g': "<875428431133810740>",
    'james': "<871742964102205480>",
    'stinky_fish': "<879257588225679390>",
    'stop': "<868861043210870794>",
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
        message.author = MockUser(id=24601)
        self.loop.run_until_complete(
            reactions.add_reactions(message, self.EMOJIS))
        message.channel.send.assert_not_called()
        message.add_reaction.assert_called_once_with(reaction)
        message.reset_mock()

  def test_mild_idea_reactions(self):
    test_cases = [
      # "thanks for a great idea",
      "oh yeah i just had an amazing idea",
      "this gives me an idea",
      "that's given me an idea",
      "i just had a terrible idea",
      "i've just had a terrible idea",
      "this image gave me a great idea…",
      "i have an idea…",
      "oh i just got an idea",
      # "oh thanks for the idea",
      "that gives me an amazingly cursed idea...",
      "that gives me an idea...",
    ]
    for text in test_cases:
      with self.subTest(msg=text):
        message = AsyncMock()
        message.content = text
        message.author = AsyncMock()
        message.author = MockUser(id=410832969599811585)
        self.loop.run_until_complete(
            reactions.add_reactions(message, self.EMOJIS))
        message.channel.send.assert_not_called()
        message.add_reaction.assert_called_once_with("<868861043210870794>")
        message.reset_mock()

  def test_mild_nonideas_dont_react(self):
    test_cases = [
      "feels like a good idea",
      "sounds like a good idea",
      "i have no idea what to say",
      "agree this does feel like a good idea.",
      "i like the lying down idea",
      "no i was more thinking “do you guys think it’s a good idea?”",
      "im sure thats a great idea",
      "anyways i have to go to bed now.",
      "yes definitely",
      "im sure thats a great idea",
      "i have no idea why",
      "usually last but i think your idea to put it in a random spot is more fun",
      "so now that you have tried to read, do you have any idea about what i’m saying.",
      "it’s kinda niche but the idea is cool, just a couple hundred years old…",
      "if anyone has any ideas of what more to change in the image ill would love to hear feedback",
      "i shouldn’t be giving advice on something where i don’t know everything but it sounds like moving is a good idea.",
      "I think you had a good idea last night.",
      "that gave you and idea right anyway me and rob also had an idea",
      "thanks for giving me help an idea i had is this",
    ]
    for text in test_cases:
      with self.subTest(msg=text):
        message = AsyncMock()
        message.content = text
        message.author = MockUser(id=410832969599811585)
        self.loop.run_until_complete(
            reactions.add_reactions(message, self.EMOJIS))
        message.channel.send.assert_not_called()
        message.add_reaction.assert_not_called()
        message.reset_mock()

  def test_non_mild_idea_doesnt_react(self):
    test_cases = [
      "oh yeah i just had an amazing idea",
      "this gives me an idea",
      "that's given me an idea",
      "i just had a terrible idea",
      "i've just had a terrible idea",
      "this image gave me a great idea…",
    ]
    for text in test_cases:
      with self.subTest(msg=text):
        message = AsyncMock()
        message.content = text
        message.author = MockUser(id=24601)
        self.loop.run_until_complete(
            reactions.add_reactions(message, self.EMOJIS))
        message.channel.send.assert_not_called()
        message.add_reaction.assert_not_called()
        message.reset_mock()
