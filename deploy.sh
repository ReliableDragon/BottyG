INSTANCE="botty-g-instance"
ZONE=us-central1-a

echo "Enter bot token: "
read TOKEN
echo $TOKEN >> token.txt

echo "Creating VM..."
gcloud compute instances create $INSTANCE \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=f1-micro \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup.sh \
    --zone $ZONE

echo "Waiting for filesystem to be created..."
sleep 30
echo "Attempting to copy token."

gcloud compute scp token.txt "botrunner@$INSTANCE:/bots/botty_g/token.txt" --zone=us-central1-a