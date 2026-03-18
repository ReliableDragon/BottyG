import asyncio
import discord
import logging
import random
import reactions
import rocket_utils

from logging.handlers import RotatingFileHandler
from collections import defaultdict
from google.cloud import secretmanager
from bot.config import (
    ALL_COUNTS_COMMAND,
    ATOMIC_FRONTIER_ID,
    DEMO_SERVER_ID,
    DISCORD_INTENTS,
    EMOJI_IDS,
    MENTION_COUNT_COMMANDS,
    MENTION_PATTERNS,
    PROJECT_ID,
    SECRET_ID,
    validate_runtime_config,
)
from bot.content import COMMANDS, QUOTES, REACTION_IMAGES, REACTION_IMAGES_MSG
from bot.handlers.commands import handle_counter_commands, handle_simple_commands
from bot.services import mentions_store
from timezone_converter import generate_time_zone_response

my_handler = RotatingFileHandler(
    'botty_g.log', mode='a', maxBytes=5*1024*1024, backupCount=2)
my_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)

MENTIONS_COLLECTION = mentions_store.MENTIONS_COLLECTION
MENTIONS_DOC = mentions_store.MENTIONS_DOC


def get_discord_token():
  client = secretmanager.SecretManagerServiceClient()
  secret_version = (
      f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest")
  response = client.access_secret_version(request={"name": secret_version})
  token = response.payload.data.decode("utf-8").strip()
  if not token:
    raise ValueError(
        f"Secret {SECRET_ID} in project {PROJECT_ID} is empty.")
  return token


def get_firestore_client():
  return mentions_store.get_firestore_client(PROJECT_ID)


def _get_firestore_increment():
  return mentions_store._get_firestore_increment()


def extract_keyword_mentions(message_text):
  return mentions_store.extract_keyword_mentions(message_text, MENTION_PATTERNS)


def increment_keyword_mentions(message_text, guild_scope=None):
  mention_counts = extract_keyword_mentions(message_text)
  if not mention_counts:
    return

  try:
    db = get_firestore_client()
    increment = _get_firestore_increment()
    updates = {
        key: increment(count) for key, count in mention_counts.items()
    }
    scope = str(guild_scope) if guild_scope is not None else mentions_store.DM_SCOPE
    db.collection(MENTIONS_COLLECTION).document(MENTIONS_DOC).collection(
        "guilds").document(scope).set(
        updates, merge=True)
  except Exception:
    logger.exception('Failed to persist keyword mention counters.')


def get_all_keyword_mention_counts(guild_scope=None):
  try:
    db = get_firestore_client()
    scope = str(guild_scope) if guild_scope is not None else mentions_store.DM_SCOPE
    snapshot = db.collection(MENTIONS_COLLECTION).document(MENTIONS_DOC).collection(
        "guilds").document(scope).get()
    data = snapshot.to_dict() if snapshot else None
    data = data or {}
    return {
        keyword: int(data.get(keyword, 0))
        for keyword in MENTION_PATTERNS.keys()
    }
  except Exception:
    logger.exception('Failed to read keyword mention counts.')
    return {keyword: 0 for keyword in MENTION_PATTERNS.keys()}


def get_keyword_mention_count(keyword, guild_scope=None):
  all_counts = get_all_keyword_mention_counts(guild_scope)
  return all_counts.get(keyword, 0)


async def increment_keyword_mentions_async(message_text, guild_scope=None):
  await asyncio.to_thread(increment_keyword_mentions, message_text, guild_scope)


async def get_all_keyword_mention_counts_async(guild_scope=None):
  return await asyncio.to_thread(get_all_keyword_mention_counts, guild_scope)


class BottyG(discord.Client):
  EMOJIS = defaultdict(lambda: 'Failed to load Atomic Frontier emojis!')

  def __init__(
      self,
      *,
      increment_mentions_async=increment_keyword_mentions_async,
      get_all_counts_async=get_all_keyword_mention_counts_async,
  ):
    super().__init__(intents=DISCORD_INTENTS)
    self._increment_mentions_async = increment_mentions_async
    self._get_all_counts_async = get_all_counts_async

  def _get_emoji(self, _id, server='atomic_frontier'):
    if server == 'atomic_frontier':
      return str(discord.utils.get(
          self.atomic_frontier.emojis, id=_id))
    elif server == 'demo_server':
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
        'stop': self._get_emoji(EMOJI_IDS['stop']),
        'james': self._get_emoji(EMOJI_IDS['james']),
    }

  async def on_ready(self):
    logger.info('Logged in as')
    logger.info(self.user.name)
    logger.info(self.user.id)
    logger.info('------')

    self.demo_server = self.get_guild(DEMO_SERVER_ID)
    if self.demo_server is None:
      logger.warning('Failed to load demo server!')

    self.atomic_frontier = self.get_guild(ATOMIC_FRONTIER_ID)
    if self.atomic_frontier is None:
      logger.warning('Failed to load Atomic Frontier data!')

    self._populate_emojis()
    self.rocketry = rocket_utils.RocketGenerator(self.EMOJIS)
    logger.info('All emojis loaded!')

  async def on_message(self, message):
    msg = message.content.lower().strip()
    cmd_token = msg.split()[0] if msg else ''
    is_command = cmd_token.startswith('!')
    guild_scope = str(message.guild.id) if getattr(message, "guild", None) else mentions_store.DM_SCOPE
    logger.info('Got a message: {}'.format(msg))

    if message.author == self.user:
      logger.info('We sent this message!')
      return

    if is_command and await handle_counter_commands(
        cmd_token=cmd_token,
        message=message,
        get_all_counts_async=self._get_all_counts_async,
        mention_count_commands=MENTION_COUNT_COMMANDS,
        all_counts_command=ALL_COUNTS_COMMAND,
    ):
      return

    if not is_command:
      await self._increment_mentions_async(message.content, guild_scope)

    if is_command:
      await self.rocketry.gen_rocket_command_responses(message)
      if await handle_simple_commands(
          cmd_token=cmd_token,
          message=message,
          logger=logger,
          quotes=QUOTES,
          reaction_images=REACTION_IMAGES,
          commands_msg=COMMANDS,
          reaction_images_msg=REACTION_IMAGES_MSG,
          randint_fn=random.randint,
      ):
        return

    if not is_command:
      await reactions.add_reactions(message, self.EMOJIS)

    time_zone_response = generate_time_zone_response(msg)
    if time_zone_response is not None:
      logger.info('Responding to time zone conversion request.')
      await message.channel.send(time_zone_response)


if __name__ == '__main__':
  validate_runtime_config()
  token = get_discord_token()
  botty_g = BottyG()
  botty_g.run(token)
