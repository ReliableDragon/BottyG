import discord
import random
import logging
import re
import reactions
import rocket_utils

from logging.handlers import RotatingFileHandler
from collections import defaultdict
from timezone_converter import generate_time_zone_response

my_handler = RotatingFileHandler(
    'botty_g.log', mode='a', maxBytes=5*1024*1024, backupCount=2)
my_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)

TOKEN = open('token.txt','r').readline()

QUOTES = (
    'It is difficult to say what is impossible, for the dream of yesterday is the hope of today and the reality of tomorrow.',
    'Just remember - when you think all is lost, the future remains.',
    'The reason many people fail is not for lack of vision but for lack of resolve and resolve is born out of counting the cost.',
    'No matter how much progress one makes, there is always the thrill of just beginning.',
    'It is not a simple matter to differentiate unsuccessful from successful experiments. . . .[Most] work that is finally successful is the result of a series of unsuccessful tests in which difficulties are gradually eliminated.',
    'But perhaps revelation often comes when you\'re not looking for it, resolution when you don\'t realize you need it.',
    'The only barrier to human development is ignorance, and this is not insurmountable.',
    'Set goals, challenge yourself, and achieve them. Live a healthy life ... and make every moment count. Rise above the obstacles, and focus on the positive.',
    'Every vision is a joke until the first man accomplishes it; once realized, it becomes commonplace.',
    'Failure crowns enterprise.',
    'Just as in the sciences we have learned that we are too ignorant to safely pronounce anything impossible, so for the individual, since we cannot know just what are his limitations, we can hardly say with certainty that anything is necessarily within or beyond his grasp.',
    'Each must remember that no one can predict to what heights of wealth, fame, or usefulness he may rise until he has honestly endeavored.',
    'It has often proved true that the dream of yesterday is the hope of today and the reality of tomorrow.'
)

BAGUETTE_CLIP = "https://cdn.discordapp.com/attachments/875464533362216960/880994913918013500/this_baguette.mp4"
SAND_CLIP = "https://cdn.discordapp.com/attachments/800703974205685790/820105727707447336/sandful_of_hand.mp4"
DANCE_CLIP = "https://cdn.discordapp.com/attachments/800703974205685790/830025367325900800/Go-James-Go.gif"

NOPE_GIF = "https://tenor.com/view/simpsons-bart-simpson-grampa-simpson-old-man-hi-bye-gif-8390063"
SYNAPSID_PIC = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Leonid_Brezhnev_and_Richard_Nixon_talks_in_1973.png/1600px-Leonid_Brezhnev_and_Richard_Nixon_talks_in_1973.png"
TIME_ZONES_GIF = "https://tenor.com/view/time-zones-wp-fairly-oddparents-gif-21690567"
BLINK_GIF = "https://tenor.com/view/umm-confused-blinking-okay-white-guy-blinking-gif-7513882"
PERFECT_GIF = "https://tenor.com/view/pacha-perfect-emperors-new-groove-very-good-gif-5346522"
AERODYNAMIC_COW_GIF = "https://tenor.com/view/cow-airflow-diagram-vectors-aerodynamics-gif-4785226"
CLAP_GIF = "https://tenor.com/view/good-job-clapping-leonardo-dicaprio-bravo-great-gif-7248435"

REACTION_IMAGES = {
    "!baguette": BAGUETTE_CLIP,
    "!snacktime": SAND_CLIP,
    "!danceparty": DANCE_CLIP,
    "!nope": NOPE_GIF,
    "!synapsid": SYNAPSID_PIC,
    "!timezones": TIME_ZONES_GIF,
    "!confusion": BLINK_GIF,
    "!perfection": PERFECT_GIF,
    "!cow": AERODYNAMIC_COW_GIF,
    "!clap": CLAP_GIF,
}

EMOJI_IDS = {
    'bobby_g': 875428431133810740,
    'spotty3': 868858496257515520,
    'spotty4': 868858506776817675,
    'spotty_fire': 871843033883213914,
    'spotty_nose_cone': 868858516687958126,
    'spotty_nose_cone_rev': 875529103984431154,
    'spotty_thruster': 871842514213142598,
    'spotty_thruster_rev': 875529093729357855,
    'stinky_fish': 879257588225679390,
    'james': 871742964102205480,
}

COMMANDS = """```
!rocket
!roorkcet
!{ro|or|ck|kc|et|te}...
!payload
!crash
!quote
!convert TIME_ZONE HH:MM TIME_ZONE...
More commands:
!reactions
```"""

REACTION_IMAGES_MSG = """```
!baguette
!snacktime
!danceparty
!synapsid
!nope
!timezones
!confusion
!perfection
!cow
!clap
```"""

ZERO_WIDTH_SPACE = "​"


class BottyG(discord.Client):
  EMOJIS = defaultdict(lambda: 'Failed to load Atomic Frontier emojis!')

  def _get_emoji(self, _id, server="atomic_frontier"):
    if server == "atomic_frontier":
      return str(discord.utils.get(
          self.atomic_frontier.emojis, id=_id))
    elif server == "demo_server":
      return str(discord.utils.get(
          self.demo_server.emojis, id=_id))

  def _populate_emojis(self):
    self.EMOJIS = {
        'bobby_g': self._get_emoji(EMOJI_IDS['bobby_g']),
        'spotty3': self._get_emoji(EMOJI_IDS['spotty3']),
        'spotty4': self._get_emoji(EMOJI_IDS['spotty4']),
        'spotty_fire': self._get_emoji(EMOJI_IDS['spotty_fire']),
        'spotty_nose_cone': self._get_emoji(EMOJI_IDS['spotty_nose_cone']),
        'spotty_nose_cone_rev': self._get_emoji(EMOJI_IDS['spotty_nose_cone_rev']),
        'spotty_thruster': self._get_emoji(EMOJI_IDS['spotty_thruster']),
        'spotty_thruster_rev': self._get_emoji(EMOJI_IDS['spotty_thruster_rev']),
        'stinky_fish': self._get_emoji(EMOJI_IDS['stinky_fish']),
        'james': self._get_emoji(EMOJI_IDS['james']),
    }

  async def on_ready(self):
    logger.info('Logged in as')
    logger.info(self.user.name)
    logger.info(self.user.id)
    logger.info('------')

    demo_server_id = 879111900485517394
    self.demo_server = self.get_guild(demo_server_id)
    if self.demo_server == None:
      logger.warning('Failed to load demo server!')

    atomic_frontier_id = 800703973890850836
    self.atomic_frontier = self.get_guild(atomic_frontier_id)
    if self.atomic_frontier == None:
      logger.warning('Failed to load Atomic Frontier data!')

    self._populate_emojis()
    self.rocketry = rocket_utils.RocketGenerator(self.EMOJIS)
    logger.info('All emojis loaded!')

  async def on_message(self, message):
    msg = message.content.lower()
    logger.info('Got a message: {}'.format(msg))

    if message.author == self.user:
      logger.info('We sent this message!')
      return

    # Rocket commands
    await self.rocketry.gen_rocket_command_responses(message)

    if msg.startswith('!advice') or msg.startswith('!quote'):
      logger.info('Sending advice.')
      rand_num = random.randint(0, len(QUOTES))
      await message.channel.send(QUOTES[rand_num])

    # Add reactions
    await reactions.add_reactions(message, self.EMOJIS)

    # Reaction images
    for key in REACTION_IMAGES:
      if msg.startswith(key):
        logger.info('Sending reaction image for {}.'.format(key))
        await message.channel.send(REACTION_IMAGES[key])

    # Timezone conversion
    time_zone_response = generate_time_zone_response(msg)
    if time_zone_response != None:
      logger.info('Responding to time zone conversion request.'.format(key))
      await message.channel.send(time_zone_response)

    # Help text
    if msg.startswith('!help') or msg.startswith('!commands'):
      logger.info('Sending command list.')
      await message.channel.send(COMMANDS)

    # Reactions list
    if msg.startswith('!reactions'):
      logger.info('Sending reaction list.')
      await message.channel.send(REACTION_IMAGES_MSG)


if __name__ == "__main__":
  botty_g = BottyG()
  botty_g.run(TOKEN)
