import discord
import random
import logging
import re

from logging.handlers import RotatingFileHandler
from collections import defaultdict

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

EMOJIS = defaultdict(lambda: 'Failed to load Atomic Frontier emojis!')
ROCKET = "Emojis failed to load!"
ROCKET_REV = "Emojis failed to load!"
ROCKET_NOSE = "Emojis failed to load!"
ROCKET_NOSE_REV = "Emojis failed to load!"
ROCKET_THRUST = "Emojis failed to load!"
ROCKET_THRUST_REV = "Emojis failed to load!"
ROCKET_BODY = "Emojis failed to load!"
ROCKET_BODY_REV = "Emojis failed to load!"

GIFS = {
    "!nope": NOPE_GIF,
    "!synapsid": SYNAPSID_PIC,
    "!timezones": TIME_ZONES_GIF,
    "!confusion": BLINK_GIF,
    "!perfection": PERFECT_GIF,
    "!cow": AERODYNAMIC_COW_GIF,
}

intents = discord.Intents.none()
intents.messages = True

client = discord.Client(intents = intents)

class BottyG(discord.Client):
    async def on_ready(self):
        global EMOJIS
        global ROCKET
        global ROCKET_REV
        global ROCKET_NOSE
        global ROCKET_NOSE_REV
        global ROCKET_THRUST
        global ROCKET_THRUST_REV
        global ROCKET_BODY
        global ROCKET_BODY_REV

        logger.info('Logged in as')
        logger.info(self.user.name)
        logger.info(self.user.id)
        logger.info('------')

        atomic_frontier_id = 800703973890850836
        atomic_frontier = self.get_guild(atomic_frontier_id)
        if atomic_frontier != None:
            logger.info('Loaded Atomic Frontier data!')
            EMOJIS = {
                'bobby_g': str(discord.utils.get(
                    atomic_frontier.emojis, id=875428431133810740)),
                'spotty4': str(discord.utils.get(
                    atomic_frontier.emojis, id=868858506776817675)),
                'spotty3': str(discord.utils.get(
                    atomic_frontier.emojis, id=868858496257515520)),
                'spotty_fire': str(discord.utils.get(
                    atomic_frontier.emojis, id=871843033883213914)),
                'spotty_nose_cone': str(discord.utils.get(
                    atomic_frontier.emojis, id=868858516687958126)),
                'spotty_nose_cone_rev': str(discord.utils.get(
                    atomic_frontier.emojis, id=875529103984431154)),
                'spotty_thruster': str(discord.utils.get(
                    atomic_frontier.emojis, id=871842514213142598)),
                'spotty_thruster_rev': str(discord.utils.get(
                    atomic_frontier.emojis, id=875529093729357855)),
                'stinky_fish': str(discord.utils.get(
                    atomic_frontier.emojis, id=879257588225679390)),
            }
            ROCKET = "{}{}{}{}{}".format(
                EMOJIS['spotty_fire'],
                EMOJIS['spotty_thruster'],
                EMOJIS['spotty3'],
                EMOJIS['spotty4'],
                EMOJIS['spotty_nose_cone'])
            ROCKET_REV = "{}{}{}{}{}".format(
                EMOJIS['spotty_nose_cone_rev'],
                EMOJIS['spotty4'],
                EMOJIS['spotty3'],
                EMOJIS['spotty_thruster_rev'],
                EMOJIS['spotty_fire'])
            ROCKET_NOSE = EMOJIS['spotty_nose_cone']
            ROCKET_NOSE_REV = EMOJIS['spotty_nose_cone_rev']
            ROCKET_THRUST = "{}{}".format(
                EMOJIS['spotty_fire'],
                EMOJIS['spotty_thruster'])
            ROCKET_THRUST_REV = "{}{}".format(
                EMOJIS['spotty_thruster_rev'],
                EMOJIS['spotty_fire'])
            ROCKET_BODY = "{}{}".format(
                EMOJIS['spotty3'],
                EMOJIS['spotty4'])
            ROCKET_BODY_REV = "{}{}".format(
                EMOJIS['spotty4'],
                EMOJIS['spotty3'])
            logger.info('All emojis loaded!')

    async def on_message(self, message):
        msg = message.content.lower()
        logger.info('Got a message: {}'.format(msg))

        if message.author == client.user:
            logger.info('We sent this message!')
            return

        # Bot commands
        elif re.match(r'^!ro{0,3}cket', msg):
            logger.info('Sending rocket')
            rocket = ROCKET_THRUST
            stop = msg.find('cket')
            rocket += ROCKET_BODY
            for _ in range(msg[:stop].count('o')):
              rocket += ROCKET_BODY
            rocket += ROCKET_NOSE
            await message.channel.send(rocket)

        elif re.match(r'^!ro{4,}cket', msg):
          rocket = ROCKET_THRUST
          rocket += ROCKET_BODY
          rocket += '💥  💥'
          rocket += ROCKET_BODY
          rocket += ROCKET_NOSE
          await message.channel.send(rocket)
          await message.channel.send('Oh the humanity!')

        elif msg.startswith('!payload'):
            payload = message.content[8:].strip()
            logger.info('Sending rocket with payload: {}'.format(payload))
            await message.channel.send(
                '{}{}{}{}{}'.format(
                    ROCKET_THRUST, ROCKET_BODY, payload, ROCKET_NOSE))

        elif msg.startswith('!crash'):
            logger.info('Sending crash.')
            await message.channel.send("{}💥{}".format(ROCKET, ROCKET_REV))

        elif msg.startswith('!advice') or msg.startswith('!quote'):
            logger.info('Sending advice.')
            rand_num = random.randint(0, len(QUOTES))
            await message.channel.send(QUOTES[rand_num])

        # Rocket mashups
        elif re.match(r'^!(?:ro|or|ck|kc|et|te){2,5}', msg):
          logger.info('Sending wonky rocket: {}'.format(msg[:11]))
          rocket_map = {
            'ro': ROCKET_THRUST,
            'or': ROCKET_THRUST_REV,
            'ck': ROCKET_BODY,
            'kc': ROCKET_BODY_REV,
            'et': ROCKET_NOSE,
            'te': ROCKET_NOSE_REV
          }
          i = 1
          wonky_rocket = ''
          while i < len(msg) and msg[i:i+2] in rocket_map:
            wonky_rocket += rocket_map[msg[i:i+2]]
            i += 2
          await message.channel.send(wonky_rocket)

        # Clips
        elif msg.startswith('!baguette'):
            logger.info('Sending baguette.')
            await message.channel.send(BAGUETTE_CLIP)

        elif msg.startswith('!snacktime'):
            logger.info('Sending sand.')
            await message.channel.send(SAND_CLIP)

        elif msg.startswith('!danceparty'):
            logger.info('Sending dancer.')
            await message.channel.send(DANCE_CLIP)

        # Historical reactions
        elif ('bobby g' in msg or
              'goddard' in msg):
            logger.info('Sending bobby g')
            await message.add_reaction(EMOJIS['bobby_g'])

        elif 'rocket' in msg and not msg.startswith('!'):
            logger.info('Reacting to rocket.')
            await message.add_reaction('🚀')

        if ('worcester polytechnic' in msg or
              'clark university' in msg):
            logger.info('Reacting to alma mater.')
            await message.add_reaction('🎓')

        if ('worcester' in msg or
              'massachusetts' in msg):
            logger.info('Reacting to home.')
            await message.add_reaction('🏠')

        if ('space' in msg or
              'astronomy' in msg or
              'mars' in msg):
            logger.info('Reacting to the stars.')
            await message.add_reaction('🔭')

        if ('war of the worlds' in msg):
            logger.info('Reacting to favorite book.')
            await message.add_reaction('📖')

        if ('sigma alpha epsilon' in msg):
            logger.info('Reacting to fraternity.')
            await message.add_reaction('🇬🇷')

        if ('tuberculosis' in msg):
            logger.info('Reacting to illness.')
            await message.add_reaction('🤒')

        # Goddard invented the precursor to the bazooka!
        if ('bazooka' in msg):
            logger.info('Reacting to bazooka.')
            await message.add_reaction('🔫')

        if ('lindbergh' in msg):
            logger.info('Reacting to friend.')
            await message.add_reaction('✈️')

        if ('roswell' in msg):
            logger.info('Reacting to roswell.')
            await message.add_reaction('👽')

        if ('esther' in msg):
            logger.info('Reacting to wife.')
            await message.add_reaction('💍')

        # Silly nonsense reactions
        if ('surstromming' in msg):
            logger.info('Reacting to stinky fish.')
            await message.add_reaction(EMOJIS['stinky_fish'])

        # Reaction images
        for key in GIFS:
          if msg.startswith(key):
              logger.info('Sending reaction image for {}.'.format(key))
              await message.channel.send(GIFS[key])

        # Help text
        if msg.startswith('!help') or msg.startswith('!commands'):
            logger.info('Sending command list.')
            await message.channel.send('https://pastebin.com/BrKtPP3w')



client = BottyG()
client.run(TOKEN)
