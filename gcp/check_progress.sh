#!/usr/bin/env bash
set -euo pipefail

INSTANCE="${INSTANCE:-botty-g-instance}"
ZONE="${ZONE:-us-central1-a}"
PROJECT_ID="${PROJECT_ID:-bottyg}"

echo "=== Startup logs (serial port) ==="
gcloud compute instances get-serial-port-output "${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}"

echo
echo "=== botty-g.service status ==="
gcloud compute ssh "botrunner@${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}" \
  --command "sudo systemctl status --no-pager botty-g.service || true"

echo
echo "=== Recent bot logs ==="
gcloud compute ssh "botrunner@${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}" \
  --command "sudo journalctl -u botty-g.service -n 100 --no-pager || true"
