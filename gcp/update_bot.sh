#!/usr/bin/env bash
set -euo pipefail

INSTANCE="${INSTANCE:-botty-g-instance}"
ZONE="${ZONE:-us-central1-a}"
PROJECT_ID="${PROJECT_ID:-bottyg}"
APP_REF="${1:-main}"

if [[ ! "${APP_REF}" =~ ^[A-Za-z0-9._/-]+$ ]]; then
  echo "Invalid APP_REF '${APP_REF}'. Use a branch, tag, or commit-ish."
  exit 1
fi

echo "Updating ${INSTANCE} in ${ZONE} to ref: ${APP_REF}"

gcloud compute ssh "botrunner@${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --zone "${ZONE}" \
  --command "sudo /bin/bash -lc '
set -euo pipefail
BOT_HOME=/bots/botty_g
RELEASES_DIR=\${BOT_HOME}/releases
REPO_DIR=\${BOT_HOME}/repo
CURRENT_LINK=\${BOT_HOME}/current
APP_REF=\"${APP_REF}\"

run_as_bot() {
  sudo -u botrunner -- \"\$@\"
}

run_as_bot git -C \${REPO_DIR} fetch --all --tags --prune
run_as_bot git -C \${REPO_DIR} checkout --detach \"\${APP_REF}\"
resolved_sha=\$(run_as_bot git -C \${REPO_DIR} rev-parse --verify HEAD)
release_dir=\${RELEASES_DIR}/\${resolved_sha}

if [[ ! -d \${release_dir} ]]; then
  mkdir -p \${release_dir}
  run_as_bot git -C \${REPO_DIR} archive \${resolved_sha} | tar -x -C \${release_dir}
  python3 -m venv \${release_dir}/env
  \${release_dir}/env/bin/pip install --upgrade pip
  \${release_dir}/env/bin/pip install -r \${release_dir}/gcp/requirements.txt
fi

ln -sfn \${release_dir} \${CURRENT_LINK}
chown -R botrunner:botrunner \${BOT_HOME}
systemctl restart botty-g.service
systemctl status --no-pager botty-g.service
'"
