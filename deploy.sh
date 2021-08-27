INSTANCE="botty-g-instance"
ZONE=us-central1-a

echo "Enter bot token: "
read TOKEN
echo $TOKEN >> token.txt

gcloud compute instances create $INSTANCE \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=f1-micro \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup.sh \
    --zone $ZONE

gcloud compute scp token.txt $INSTANCE:/bots/botty_g/token.txt