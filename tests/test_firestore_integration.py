import os
import uuid

import pytest

from bot.config import MENTIONS_COLLECTION, MENTIONS_DOC, PROJECT_ID
from bot.services import mentions_store


def _should_run_firestore_integration():
  return os.getenv("BOTTYG_RUN_FIRESTORE_IT") == "1"


@pytest.mark.integration
def test_firestore_mentions_round_trip():
  if not _should_run_firestore_integration():
    pytest.skip("Set BOTTYG_RUN_FIRESTORE_IT=1 to run Firestore integration tests.")
  if not os.getenv("FIRESTORE_EMULATOR_HOST"):
    pytest.skip("Set FIRESTORE_EMULATOR_HOST to run Firestore integration tests.")

  # Point to a unique document for test isolation.
  test_doc = f"{MENTIONS_DOC}_{uuid.uuid4().hex}"
  client = mentions_store.get_firestore_client(PROJECT_ID)
  doc = client.collection(MENTIONS_COLLECTION).document(test_doc)

  doc.set({"rocket": 0, "james": 0, "loss": 0})
  doc.set({"rocket": 2, "james": 1}, merge=True)
  snapshot = doc.get()
  data = snapshot.to_dict() or {}

  assert data.get("rocket") == 2
  assert data.get("james") == 1
  assert data.get("loss") == 0

