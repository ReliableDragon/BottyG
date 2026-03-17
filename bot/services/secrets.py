from google.cloud import secretmanager


def get_discord_token(project_id, secret_id):
  client = secretmanager.SecretManagerServiceClient()
  secret_version = (
      f"projects/{project_id}/secrets/{secret_id}/versions/latest")
  response = client.access_secret_version(request={"name": secret_version})
  token = response.payload.data.decode("utf-8").strip()
  if not token:
    raise ValueError(
        f"Secret {secret_id} in project {project_id} is empty.")
  return token

