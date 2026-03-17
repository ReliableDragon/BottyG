import os
import re

import discord

def _get_env_int(name, default):
  raw = os.getenv(name)
  if raw is None or raw.strip() == "":
    return default
  try:
    return int(raw)
  except ValueError as exc:
    raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


PROJECT_ID = os.getenv("BOTTYG_PROJECT_ID", "bottyg").strip()
SECRET_ID = os.getenv("BOTTYG_SECRET_ID", "discord_bot_token").strip()

MENTIONS_COLLECTION = os.getenv("BOTTYG_MENTIONS_COLLECTION", "stats").strip()
MENTIONS_DOC = os.getenv("BOTTYG_MENTIONS_DOC", "mention_counts").strip()

MENTION_PATTERNS = {
    "rocket": re.compile(r"\brockets?\b"),
    "james": re.compile(r"\bjames(?:'s)?\b"),
    "loss": re.compile(r"\bloss\b"),
}

MENTION_COUNT_COMMANDS = {
    "!rocket_count": "rocket",
    "!james_count": "james",
    "!loss_count": "loss",
}
ALL_COUNTS_COMMAND = "!counts"

DEMO_SERVER_ID = _get_env_int("BOTTYG_DEMO_SERVER_ID", 879111900485517394)
ATOMIC_FRONTIER_ID = _get_env_int("BOTTYG_ATOMIC_FRONTIER_ID", 800703973890850836)
MILD_USER_ID = _get_env_int("BOTTYG_MILD_USER_ID", 410832969599811585)

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
    'stop': 868861043210870794,
}

DISCORD_INTENTS = discord.Intents.default()
DISCORD_INTENTS.message_content = True


def validate_runtime_config():
  if not PROJECT_ID:
    raise ValueError("BOTTYG_PROJECT_ID cannot be empty.")
  if not SECRET_ID:
    raise ValueError("BOTTYG_SECRET_ID cannot be empty.")
  if not MENTIONS_COLLECTION:
    raise ValueError("BOTTYG_MENTIONS_COLLECTION cannot be empty.")
  if not MENTIONS_DOC:
    raise ValueError("BOTTYG_MENTIONS_DOC cannot be empty.")
