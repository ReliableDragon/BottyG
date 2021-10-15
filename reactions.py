import logging
import re


async def add_reactions(message, emojis):
  logger = logging.getLogger("root")
  msg = message.content.lower()
  # Historical reactions
  if ('bobby g' in msg or
      'goddard' in msg):
    logger.info('Sending bobby g')
    await message.add_reaction(emojis['bobby_g'])

  if 'rocket' in msg and not msg.startswith('!'):
    logger.info('Reacting to rocket.')
    await message.add_reaction('🚀')

  if ('worcester polytechnic' in msg or
    'clark university' in msg):
    logger.info('Reacting to alma mater.')
    await message.add_reaction('🎓')

  if (('worcester' in msg and
      not 'worcester polytechnic' in msg) or
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

  if ('nahum' in msg):
    logger.info('Reacting to father.')
    await message.add_reaction('👨‍👦')

  # Silly server related reactions
  if ('james' in msg):
    logger.info('Reacting to james.')
    await message.add_reaction(emojis['james'])

  if ('surstromming' in msg):
    logger.info('Reacting to stinky fish.')
    await message.add_reaction(emojis['stinky_fish'])

  # React to Mild's ideas. ;)
  # name="󠇰 󠇰", discriminator="8273"
  # id: 410832969599811585
  # my id: 466722871733911553
  if message.author.id == 410832969599811585:
    msg = ''.join([c for c in msg if c == ' ' or c.isalpha()])
    idea_phrases = [
      r"(?:i|ive) (?:(?!(?:not?|you|he|she|they)\b)\w+ )*(?:had|have|got|came up with|(?:(?:you|he|she|they|it|this) (?:(?!not?\b)\w+ )*gave (?:(?!no\b)\w+ )*me)) (?:(?!no\b)\w+ )*idea",
      r"(?:gave|giv\w+) me (?:an?) (?:(?!(?:not?)\b)\w+ ){0,3}idea",
      # r"thanks for (?:(?!(?:not?|you|he|she|they)\b)\w+ )*idea",
    ]
    if any([re.search(pattern, msg) for pattern in idea_phrases]):
      await message.add_reaction(emojis['stop'])
