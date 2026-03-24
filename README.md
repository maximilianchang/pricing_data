# pricing_data

## Deployment

Make sure Docker is in your PATH first:
```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
```

Build the image:
```bash
DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build \
  -t us-west1-docker.pkg.dev/scraping-engine-488601/scrapers/scraping-engine:latest \
  .
```

Push to Artifact Registry:
```bash
docker push us-west1-docker.pkg.dev/scraping-engine-488601/scrapers/scraping-engine:latest
```
