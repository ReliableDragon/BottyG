#!/usr/bin/env bash
set -euxo pipefail

BOT_USER="botrunner"
BOT_HOME="/bots/botty_g"
RELEASES_DIR="${BOT_HOME}/releases"
REPO_DIR="${BOT_HOME}/repo"
CURRENT_LINK="${BOT_HOME}/current"
SYSTEMD_UNIT="/etc/systemd/system/botty-g.service"

METADATA_URL="http://metadata.google.internal/computeMetadata/v1/instance/attributes"
METADATA_HEADER="Metadata-Flavor: Google"

APP_REPO="$(curl -fsS -H "${METADATA_HEADER}" "${METADATA_URL}/APP_REPO")"
APP_REF="$(curl -fsS -H "${METADATA_HEADER}" "${METADATA_URL}/APP_REF" || true)"
if [[ -z "${APP_REF}" ]]; then
  APP_REF="main"
fi

if ! id -u "${BOT_USER}" >/dev/null 2>&1; then
  useradd -m -d "/home/${BOT_USER}" "${BOT_USER}"
fi

run_as_bot() {
  sudo -u "${BOT_USER}" -- "$@"
}

mkdir -p "${RELEASES_DIR}" "${REPO_DIR}"
chown -R "${BOT_USER}:${BOT_USER}" "${BOT_HOME}"

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -yq git python3 python3-venv python3-pip

if [[ ! -d "${REPO_DIR}/.git" ]]; then
  run_as_bot git clone "${APP_REPO}" "${REPO_DIR}"
fi

run_as_bot git -C "${REPO_DIR}" fetch --all --tags --prune
deploy_ref="${APP_REF}"
if run_as_bot git -C "${REPO_DIR}" show-ref --verify --quiet "refs/remotes/origin/${APP_REF}"; then
  deploy_ref="origin/${APP_REF}"
fi

run_as_bot git -C "${REPO_DIR}" checkout --detach "${deploy_ref}"
resolved_sha="$(run_as_bot git -C "${REPO_DIR}" rev-parse --verify HEAD)"

# Use commit SHA for immutable release directory names.
release_dir="${RELEASES_DIR}/${resolved_sha}"
if [[ ! -d "${release_dir}" ]]; then
  mkdir -p "${release_dir}"
  run_as_bot git -C "${REPO_DIR}" archive "${resolved_sha}" | tar -x -C "${release_dir}"
  python3 -m venv "${release_dir}/env"
  "${release_dir}/env/bin/pip" install --upgrade pip
  "${release_dir}/env/bin/pip" install -r "${release_dir}/gcp/requirements.txt"
fi

ln -sfn "${release_dir}" "${CURRENT_LINK}"
chown -R "${BOT_USER}:${BOT_USER}" "${BOT_HOME}"

cat > "${SYSTEMD_UNIT}" <<'EOF'
[Unit]
Description=BottyG Discord bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=botrunner
Group=botrunner
WorkingDirectory=/bots/botty_g/current
ExecStart=/bots/botty_g/current/env/bin/python3 /bots/botty_g/current/botty_g.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable botty-g.service
systemctl restart botty-g.service
