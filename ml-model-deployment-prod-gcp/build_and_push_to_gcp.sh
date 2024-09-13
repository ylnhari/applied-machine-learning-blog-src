# Authenticate with GCP
gcloud auth login

# Set the Project
export PROJECT_ID=$(gcloud config get-value project)

#Replace region, your-image-name and $TAG_NAME with appropriate values.
export CONTAINER_LINK = <region>.pkg.dev/$PROJECT_ID/custom-image-registry/your-image-name:$TAG_NAME

#Build the Docker Image , 
docker build -t  $CONTAINER_LINK Dockerfile.dockerfile .

#Push the Image to GCR
docker push $CONTAINER_LINK
