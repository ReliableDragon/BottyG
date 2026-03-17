# Set context
PROJECT_ID="bottyg"
SECRET_ID="discord_bot_token"

gcloud config set project "$PROJECT_ID"

# (One-time per project) enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create the secret container (run once per secret)
gcloud secrets create "$SECRET_ID" --replication-policy="automatic"

# Add secret value from token.txt as a new version
gcloud secrets versions add "$SECRET_ID" --data-file="token.txt"

-------

PROJECT_ID="bottyg"
RUNTIME_SA="botty-g-runtime@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud config set project "${PROJECT_ID}"
gcloud services enable compute.googleapis.com secretmanager.googleapis.com logging.googleapis.com

gcloud iam service-accounts create botty-g-runtime \
  --display-name="BottyG Runtime" || true

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding discord_bot_token \
  --member="serviceAccount:${RUNTIME_SA}" \
  --role="roles/secretmanager.secretAccessor"

-------

cd /Users/gabe/Documents/BottyG
./gcp/deploy.sh main
./gcp/check_progress.sh

-------

cd /Users/gabe/Documents/BottyG

INSTANCE="botty-g-instance"
ZONE="us-central1-a"
PROJECT_ID="bottyg"

gcloud config set project "${PROJECT_ID}"

gcloud compute scp gcp/startup.sh "botrunner@${INSTANCE}:/tmp/startup.sh" --zone "${ZONE}"
gcloud compute ssh "botrunner@${INSTANCE}" --zone "${ZONE}" --command "sudo bash /tmp/startup.sh"
./gcp/check_progress.sh

-------

./gcp/update_bot.sh main
./gcp/check_progress.sh