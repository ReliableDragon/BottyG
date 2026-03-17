# BottyG GCP Deployment

## One-time project setup

```bash
PROJECT_ID="bottyg"
RUNTIME_SA="botty-g-runtime@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud config set project "${PROJECT_ID}"
gcloud services enable compute.googleapis.com secretmanager.googleapis.com logging.googleapis.com

gcloud iam service-accounts create botty-g-runtime \
  --display-name="BottyG Runtime"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding discord_bot_token \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/secretmanager.secretAccessor"
```

## Initial deploy

```bash
./gcp/deploy.sh main
./gcp/check_progress.sh
```

`deploy.sh` resolves refs from the configured repo URL. By default it uses your local git `origin` URL.

## Update deploy (pin to branch, tag, or commit)

```bash
./gcp/update_bot.sh main
./gcp/update_bot.sh <git-commit-sha>
```

Before running update, make sure the target ref is pushed to the remote repository.

## Rollback

```bash
./gcp/update_bot.sh <previous-git-commit-sha>
```

## Teardown

```bash
./gcp/teardown.sh
```
