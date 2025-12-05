# ASCII Chicken IP Service 🐔

A simple, lightweight service that returns your public IP address and a friendly ASCII chicken. Inspired by `icanhazip.com` and `ipchicken.com`.

## Usage

```bash
curl https://icanhazchicken.com
```

**Output:**
```
203.0.113.1
   \\
   (o>
\\_//)
 \_/_)
  _|_
```

## Features
- **Plain Text Output**: Perfect for CLI usage with `curl` or `wget`.
- **Smart IP Detection**: 
  - Returns the client's public IP when running in the cloud (respects `X-Forwarded-For`).
  - Fetches the network's public IP (via `api.ipify.org`) when running locally or in Docker, so you always see your real public IP.
- **Dockerized**: Ready to deploy anywhere.

## Running Locally

### Python
```bash
python3 server.py
```
The server will start on port **8081**.

### Docker
```bash
docker-compose up --build
```

## Deployment

### Google Cloud Run (Recommended)
This service is stateless and perfect for Cloud Run's free tier.

```bash
gcloud run deploy ascii-chicken --source . --port 8081 --allow-unauthenticated
```

### Fly.io
```bash
fly launch
fly deploy
```

## License
MIT
