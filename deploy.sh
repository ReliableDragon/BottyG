MY_INSTANCE_NAME="botty-g-instance"
ZONE=us-central1-a

gcloud compute instances create $MY_INSTANCE_NAME \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=f1-micro \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup.sh \
    --zone $ZONE