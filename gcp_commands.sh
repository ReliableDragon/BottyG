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
