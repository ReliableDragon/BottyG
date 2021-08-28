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
)

BAGUETTE_CLIP = "https://cdn.discordapp.com/attachments/875464533362216960/880994913918013500/this_baguette.mp4"
SAND_CLIP = "https://cdn.discordapp.com/attachments/800703974205685790/820105727707447336/sandful_of_hand.mp4"

EMOJIS = defaultdict(lambda: 'Failed to load Atomic Frontier emojis!')
ROCKET = "Emojis failed to load!"
ROCKET_REV = "Emojis failed to load!"
ROCKET_NOSE = "Emojis failed to load!"
ROCKET_NOSE_REV = "Emojis failed to load!"
ROCKET_THRUST = "Emojis failed to load!"
ROCKET_THRUST_REV = "Emojis failed to load!"
ROCKET_BODY = "Emojis failed to load!"
ROCKET_BODY_REV = "Emojis failed to load!"

intents = discord.Intents.none()
intents.messages = True

client = discord.Client(intents = intents)

class BottyG(discord.Client):
    async def on_ready(self):
        global EMOJIS
        global ROCKET
        global ROCKET_REV
        global ROCKET_THRUST
        global ROCKET_THRUST_REV
        global ROCKET_BODY
        global ROCKET_BODY_REV
        global ROCKET_NOSE
        global ROCKET_NOSE_REV

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
            }
            ROCKET = "{}{}{}{}{}{}{}".format(
                EMOJIS['spotty_fire'],
                EMOJIS['spotty_thruster'],
                EMOJIS['spotty3'],
                EMOJIS['spotty4'],
                EMOJIS['spotty_nose_cone'])
            ROCKET_REV = "{}{}{}{}{}{}{}".format(
                EMOJIS['spotty_nose_cone_rev'],
                EMOJIS['spotty4'],
                EMOJIS['spotty3'],
                EMOJIS['spotty_thruster_rev'],
                EMOJIS['spotty_fire'])
            ROCKET_NOSE = EMOJIS['spotty_nose_cone']
            ROCKET_NOSE_REV = EMOJIS['spotty_nose_cone']
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

    async def on_message(self, message):
        msg = message.content.lower()
        logger.info('Got a message: {}'.format(msg))

        if message.author == client.user:
            logger.info('We sent this message!')
            return

        if re.match(r'^!ro{0,3}cket', msg):
            logger.info('Sending rocket')
            rocket = ROCKET_THRUST
            stop = msg.find('cket')
            rocket += ROCKET_BODY
            for _ in range(msg[:stop]).count('o'):
              rocket += ROCKET_BODY
            rocket += ROCKET_NOSE
            await message.channel.send(rocket)

        if (msg.find('bobby g') != -1 or
            msg.find('goddard') != -1):
            logger.info('Sending bobby g')
            await message.add_reaction(EMOJIS['bobby_g'])

        if msg.startswith('!payload'):
            payload = message.content[8:].strip()
            logger.info('Sending rocket with payload: {}'.format(payload))
            await message.channel.send(
                '{}{}{}{}'.format(
                    ROCKET_THRUST, ROCKET_BODY, payload, ROCKET_NOSE))

        if msg.startswith('!advice'):
            logger.info('Sending advice.')
            rand_num = random.randint(0, len(QUOTES))
            await message.channel.send(QUOTES[rand_num])

        if msg.startswith('!crash'):
            logger.info('Sending crash.')
            await message.channel.send("{}💥{}".format(ROCKET, ROCKET_REV))

        if msg.startswith('!baguette'):
            logger.info('Sending baguette.')
            await message.channel.send(BAGUETTE_CLIP)

        if msg.startswith('!snacktime'):
            logger.info('Sending sand.')
            await message.channel.send(SAND_CLIP)


client = BottyG()
client.run(TOKEN)
