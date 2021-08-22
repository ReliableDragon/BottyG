import discord
import random

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

EMOJIS = None
ROCKET_MESSAGE = None
ROCKET_BASE = None

intents = discord.Intents.none()
intents.messages = True

client = discord.Client(intents = intents)

class BottyG(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        atomic_frontier_id = 800703973890850836
        atomic_frontier = self.get_guild(atomic_frontier_id)

        EMOJIS = {
            'bobby_g': discord.utils.get(atomic_frontier.emojis, id=875428431133810740),
            'spotty2': discord.utils.get(atomic_frontier.emojis, id=868858506776817675),
            'spotty3': discord.utils.get(atomic_frontier.emojis, id=868858496257515520),
            'spotty_fire': discord.utils.get(atomic_frontier.emojis, id=868858516687958126),
            'spotty_nose_cone': discord.utils.get(atomic_frontier.emojis, id=868858516687958126),
            'spotty_thruster': discord.utils.get(atomic_frontier.emojis, id=871842514213142598),
        }
        ROCKET_MESSAGE = f"{EMOJIS['spotty_fire']} {EMOJIS['spotty_thruster']} {EMOJIS['spotty2']} {EMOJIS['spotty3']} {EMOJIS['spotty2']} {EMOJIS['spotty3']} {EMOJIS['spotty_nose_cone']}"
        ROCKET_BASE = f"{EMOJIS['spotty_fire']} {EMOJIS['spotty_thruster']} {EMOJIS['spotty2']} {EMOJIS['spotty3']}"

    async def on_message(self, message):
        print('Got a message!')

        if message.author == client.user:
            return

        if message.content.startswith('!rocket'):
            print('Sending rocket')
            await message.channel.send(ROCKET_MESSAGE)

        if message.content.lower().find('bobby g') != -1:
            print('Sending bobby g')
            await message.add_reaction(EMOJIS['bobby_g'])

        if message.content.startswith('!payload'):
            payload = message.content[9:]
            print(f'Sending rocket with payload: {payload}')
            await message.channel.send(ROCKET_BASE + f' {payload} {EMOJIS["spotty_nose_cone"]}')

        if message.content.startswith('!advice'):
            rand_num = random.randint(0, len(QUOTES))
            await message.channel.send(QUOTES[rand_num])


client = BottyG()
client.run(TOKEN)
