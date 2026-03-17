#!/usr/bin/env bash
set -euo pipefail

INSTANCE="${INSTANCE:-botty-g-instance}"
ZONE="${ZONE:-us-central1-a}"
PROJECT_ID="${PROJECT_ID:-bottyg}"

gcloud compute instances delete "${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}" \
  --delete-disks=all
