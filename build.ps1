# build.ps1

# 1. Compile SCSS (Assumes you have sass installed via npm or choco)
# If you use a python script to compile, change this to: python compile_scss.py
Write-Host "Compiling SCSS..." -ForegroundColor Yellow
python app/site/src/builderCss.py

# 2. Build the Docker Image
Write-Host "Building Docker Image..." -ForegroundColor Cyan
docker build -t flask-app .

Write-Host "Tagging for Docker Hub..." -ForegroundColor Magenta
docker tag flask-app capydev/flask-app:latest

Write-Host "Pushing to Docker Hub..." -ForegroundColor Blue
docker push capydev/flask-app:latest

Write-Host "Done! Run 'docker run -p 8000:8000 flask-app' to start." -ForegroundColor Green