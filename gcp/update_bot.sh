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

if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git fetch --quiet origin || true

  if [[ -n "$(git status --porcelain)" ]]; then
    echo "WARNING: You have uncommitted local changes that are not deployable via remote refs."
  fi

  if git show-ref --verify --quiet "refs/heads/${APP_REF}" && \
     git show-ref --verify --quiet "refs/remotes/origin/${APP_REF}"; then
    ahead_count="$(git rev-list --count "origin/${APP_REF}..${APP_REF}")"
    behind_count="$(git rev-list --count "${APP_REF}..origin/${APP_REF}")"

    if [[ "${ahead_count}" -gt 0 ]]; then
      echo "WARNING: Local branch '${APP_REF}' is ahead of origin/${APP_REF} by ${ahead_count} commit(s)."
      echo "WARNING: Push your changes if you want them included in this deploy."
    fi
    if [[ "${behind_count}" -gt 0 ]]; then
      echo "WARNING: Local branch '${APP_REF}' is behind origin/${APP_REF} by ${behind_count} commit(s)."
    fi
  fi
else
  echo "WARNING: Not running from a local git repo; unable to check for unpushed changes."
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

chown -R botrunner:botrunner \${BOT_HOME}
run_as_bot git -C \${REPO_DIR} fetch --all --tags --prune
deploy_ref=\${APP_REF}
if run_as_bot git -C \${REPO_DIR} show-ref --verify --quiet \"refs/remotes/origin/\${APP_REF}\"; then
  deploy_ref=\"origin/\${APP_REF}\"
fi

run_as_bot git -C \${REPO_DIR} checkout --detach \"\${deploy_ref}\"
resolved_sha=\$(run_as_bot git -C \${REPO_DIR} rev-parse --verify HEAD)
release_dir=\${RELEASES_DIR}/\${resolved_sha}

if [[ ! -d \${release_dir} ]]; then
  mkdir -p \${release_dir}
  run_as_bot git -C \${REPO_DIR} archive \${resolved_sha} | tar -x -C \${release_dir}
  chown -R botrunner:botrunner \${release_dir}
  python3 -m venv \${release_dir}/env
  \${release_dir}/env/bin/pip install --upgrade pip
  \${release_dir}/env/bin/pip install -r \${release_dir}/gcp/requirements.txt
fi

ln -sfn \${release_dir} \${CURRENT_LINK}
chown -R botrunner:botrunner \${BOT_HOME}
systemctl restart botty-g.service
systemctl status --no-pager botty-g.service
'"
