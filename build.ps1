# build.ps1

# Stop the script if any command fails
$ErrorActionPreference = "Stop"

$IMAGE_NAME = "flask-app"
$DOCKER_HUB_REPO = "capydev/flask-app"

# 1. Compile SCSS
Write-Host "--- Compiling SCSS ---" -ForegroundColor Yellow
python app/site/src/builderCss.py

# 2. Build the Docker Image
Write-Host "--- Building Docker Image ---" -ForegroundColor Cyan
docker build -t "${DOCKER_HUB_REPO}:latest" .

Write-Host "--- Pushing to Docker Hub ---" -ForegroundColor Blue
docker push "${DOCKER_HUB_REPO}:latest"

Write-Host "--- Done! ---" -ForegroundColor Green
Write-Host "Run 'docker run -p 8000:8000 $IMAGE_NAME' to start locally." 