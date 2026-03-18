import asyncio
import logging

from bot.config import MENTIONS_COLLECTION, MENTIONS_DOC, MENTION_PATTERNS

logger = logging.getLogger('root')

_firestore_client = None
DM_SCOPE = "dm"


def get_firestore_client(project_id):
  global _firestore_client
  if _firestore_client is not None:
    return _firestore_client

  import firebase_admin
  from firebase_admin import firestore

  try:
    firebase_admin.get_app()
  except ValueError:
    firebase_admin.initialize_app(options={"projectId": project_id})

  _firestore_client = firestore.client()
  return _firestore_client


def _get_firestore_increment():
  from firebase_admin import firestore
  return firestore.Increment


def _normalize_scope(guild_scope):
  if guild_scope is None:
    return DM_SCOPE
  return str(guild_scope)


def _guild_doc(db, guild_scope):
  scope = _normalize_scope(guild_scope)
  return (
      db.collection(MENTIONS_COLLECTION)
      .document(MENTIONS_DOC)
      .collection("guilds")
      .document(scope)
  )


def extract_keyword_mentions(message_text, patterns=MENTION_PATTERNS):
  msg = message_text.lower()
  return {
      key: len(pattern.findall(msg))
      for key, pattern in patterns.items()
      if pattern.search(msg)
  }


def increment_keyword_mentions(message_text, project_id, guild_scope=None):
  mention_counts = extract_keyword_mentions(message_text)
  if not mention_counts:
    return

  try:
    db = get_firestore_client(project_id)
    increment = _get_firestore_increment()
    updates = {
        key: increment(count) for key, count in mention_counts.items()
    }
    _guild_doc(db, guild_scope).set(updates, merge=True)
  except Exception:
    logger.exception("Failed to persist keyword mention counters.")


def get_all_keyword_mention_counts(
    project_id, guild_scope=None, keys=MENTION_PATTERNS.keys()):
  try:
    db = get_firestore_client(project_id)
    snapshot = _guild_doc(db, guild_scope).get()
    data = snapshot.to_dict() if snapshot else None
    data = data or {}
    return {
        keyword: int(data.get(keyword, 0))
        for keyword in keys
    }
  except Exception:
    logger.exception("Failed to read keyword mention counts.")
    return {keyword: 0 for keyword in keys}


async def increment_keyword_mentions_async(message_text, project_id, guild_scope=None):
  await asyncio.to_thread(
      increment_keyword_mentions, message_text, project_id, guild_scope)


async def get_all_keyword_mention_counts_async(project_id, guild_scope=None):
  return await asyncio.to_thread(
      get_all_keyword_mention_counts, project_id, guild_scope)
