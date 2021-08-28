import discord
import random
import logging
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
EMOJIS = defaultdict(lambda: 'Failed to load Atomic Frontier emojis!')
ROCKET_MESSAGE = "Rocket failed to load!"
ROCKET_BASE = "Rocket base failed to load!"
# RBP_ROCKET = "RBP rocket failed to load!"
# RBP_EMOJI = "RBP emoji failed to load!"

intents = discord.Intents.none()
intents.messages = True

client = discord.Client(intents = intents)

class BottyG(discord.Client):
    async def on_ready(self):
        # global RBP_EMOJI
        # global RBP_ROCKET
        global EMOJIS
        global ROCKET_MESSAGE
        global ROCKET_BASE

        logger.info('Logged in as')
        logger.info(self.user.name)
        logger.info(self.user.id)
        logger.info('------')

        # rbp_id = 879111900485517394
        # rbp = self.get_guild(rbp_id)
        # logger.info('rbp guild: {}'.format(rbp))
        # RBP_EMOJI = str(discord.utils.get(rbp.emojis, id=879130415502360636))
        # logger.info('RBP Emoji: {}'.format(RBP_EMOJI))
        # RBP_ROCKET = "{} {} {} {}".format(
        #     RBP_EMOJI,
        #     RBP_EMOJI,
        #     RBP_EMOJI,
        #     RBP_EMOJI)
        # logger.info('RBP Rocket: {}'.format(RBP_ROCKET))

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
                'spotty_thruster': str(discord.utils.get(
                    atomic_frontier.emojis, id=871842514213142598)),
            }
            ROCKET_MESSAGE = "{}{}{}{}{}{}{}".format(
                EMOJIS['spotty_fire'],
                EMOJIS['spotty_thruster'],
                EMOJIS['spotty3'],
                EMOJIS['spotty4'],
                EMOJIS['spotty3'],
                EMOJIS['spotty4'],
                EMOJIS['spotty_nose_cone'])
            ROCKET_BASE = "{}{}{}{}".format(
                EMOJIS['spotty_fire'],
                EMOJIS['spotty_thruster'],
                EMOJIS['spotty3'],
                EMOJIS['spotty4'])

    async def on_message(self, message):
        msg = message.content.lower()
        logger.info('Got a message: {}'.format(msg))

        if message.author == client.user:
            logger.info('We sent this message!')
            return

        # if msg.startswith('!debug_rocket'):
        #     logger.info('Sending debug rocket: {}'.format(RBP_ROCKET))
        #     await message.channel.send(RBP_ROCKET)
        #
        # if msg.startswith('!debug_payload'):
        #     logger.info('Sending debug payload')
        #     payload = message.content[14:]
        #     await message.channel.send(
        #         '{} {} {}'.format(RBP_ROCKET, payload, RBP_EMOJI))
        #
        # if msg.find('H5XGD54XI4N18LVTR8M594DRT2JNMOW5'.lower()) != -1:
        #     logger.info('Sending debug reaction')
        #     await message.add_reaction(RBP_EMOJI)

        if msg.startswith('!rocket'):
            logger.info('Sending rocket')
            await message.channel.send(ROCKET_MESSAGE)

        if (msg.find('bobby g') != -1 or
            msg.find('goddard') != -1):
            logger.info('Sending bobby g')
            await message.add_reaction(EMOJIS['bobby_g'])

        if msg.startswith('!payload'):
            payload = message.content[8:].strip()
            logger.info('Sending rocket with payload: {}'.format(payload))
            await message.channel.send(
                '{}{}{}'.format(
                    ROCKET_BASE, payload, EMOJIS["spotty_nose_cone"]))

        if msg.startswith('!advice'):
            logger.info('Sending advice.')
            rand_num = random.randint(0, len(QUOTES))
            await message.channel.send(QUOTES[rand_num])

        if msg.startswith('!baguette'):
            logger.info('Sending baguette.')
            await message.channel.send(BAGUETTE_CLIP)


client = BottyG()
client.run(TOKEN)
