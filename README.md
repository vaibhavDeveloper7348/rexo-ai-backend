# REXO AI Backend - Flask APIs

Backend services for REXO AI mobile application.

## Services

- **Jack AI** (Port 5001): Voice assistant with GNDEC FAQs
- **Jarvis AI** (Port 5002): Smart search and calculations
- **SQL Guard** (Port 5003): SQL injection detection

## Deployment

Deployed on Render.com

## API Endpoints

### Jack AI
- GET /jack/health
- POST /jack/command

### Jarvis AI
- POST /jarvis/command

### SQL Guard
- POST /sql/scan_query
- POST /sql/scan_file