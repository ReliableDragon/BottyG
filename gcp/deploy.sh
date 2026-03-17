#!/usr/bin/env bash
set -euo pipefail

INSTANCE="${INSTANCE:-botty-g-instance}"
ZONE="${ZONE:-us-central1-a}"
MACHINE_TYPE="${MACHINE_TYPE:-e2-micro}"
PROJECT_ID="${PROJECT_ID:-bottyg}"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_EMAIL:-botty-g-runtime@${PROJECT_ID}.iam.gserviceaccount.com}"
DEFAULT_APP_REPO="$(git config --get remote.origin.url || true)"
if [[ -z "${DEFAULT_APP_REPO}" ]]; then
  DEFAULT_APP_REPO="https://github.com/SethBorder/BottyG.git"
fi
APP_REPO="${APP_REPO:-${DEFAULT_APP_REPO}}"
APP_REF="${1:-main}"

if [[ ! "${APP_REF}" =~ ^[A-Za-z0-9._/-]+$ ]]; then
  echo "Invalid APP_REF '${APP_REF}'. Use a branch, tag, or commit-ish."
  exit 1
fi

echo "Deploy settings:"
echo "  PROJECT_ID=${PROJECT_ID}"
echo "  INSTANCE=${INSTANCE}"
echo "  ZONE=${ZONE}"
echo "  MACHINE_TYPE=${MACHINE_TYPE}"
echo "  SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_EMAIL}"
echo "  APP_REPO=${APP_REPO}"
echo "  APP_REF=${APP_REF}"

gcloud config set project "${PROJECT_ID}"

echo "Creating VM with startup automation..."
gcloud compute instances create "${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}" \
  --machine-type "${MACHINE_TYPE}" \
  --image-family debian-12 \
  --image-project debian-cloud \
  --service-account "${SERVICE_ACCOUNT_EMAIL}" \
  --scopes https://www.googleapis.com/auth/cloud-platform \
  --metadata "APP_REPO=${APP_REPO},APP_REF=${APP_REF}" \
  --metadata-from-file startup-script=gcp/startup.sh

echo "Instance created. Check bootstrap logs with:"
echo "gcloud compute instances get-serial-port-output ${INSTANCE} --zone ${ZONE}"
