# Authenticate with GCP
gcloud auth login

# Set the Project
export PROJECT_ID=$(gcloud config get-value project)

# Build the Docker Image , Replace ,region, your-image-name and $TAG_NAME with appropriate values.
docker build -t <region>.pkg.dev/$PROJECT_ID/custom-image-registry/your-image-name:$TAG_NAME .

#Push the Image to GCR:
gcloud auth configure-docker
docker push gcr.io/$PROJECT_ID/your-image-name:$TAG_NAME
