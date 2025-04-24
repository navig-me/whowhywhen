# WhoWhyWhen API Documentation

This document describes the API endpoints available in WhoWhyWhen.

## Base URLs

- API: `http://localhost:8001/api`
- Dashboard API: `http://localhost:8000/dashapi`

## Authentication

Most endpoints require authentication using either:

1. **JWT Token** (for dashboard API)
   - Obtained by logging in through `/dashauth/token`
   - Passed in the `Authorization` header as `Bearer {token}`

2. **API Key** (for tracking API)
   - Generated in the dashboard
   - Passed in the `X-API-KEY` header

## Dashboard API Endpoints

### Authentication

#### Login

```
POST /dashauth/token
```

Request body:
```json
{
  "username": "your.email@example.com",
  "password": "your_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Register

```
POST /dashauth/register
```

Request body:
```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "password": "your_password",
  "project_name": "My Project"
}
```

### User

#### Get Current User

```
GET /dashauth/users/me
```

Headers:
```
Authorization: Bearer {token}
```

### Projects

#### List User Projects

```
GET /dashauth/users/me/projects
```

Headers:
```
Authorization: Bearer {token}
```

#### Create Project

```
POST /dashauth/users/me/projects?project_name=New%20Project
```

Headers:
```
Authorization: Bearer {token}
```

### API Keys

#### List API Keys

```
GET /dashapi/apikeys
```

Headers:
```
Authorization: Bearer {token}
```

#### Create API Key

```
POST /dashapi/apikeys?project_id=your-project-id
```

Headers:
```
Authorization: Bearer {token}
```

#### Delete API Key

```
DELETE /dashapi/apikeys/{api_key_id}
```

Headers:
```
Authorization: Bearer {token}
```

### Logs

#### Get API Logs

```
GET /dashapi/logs?project_id=your-project-id&page=1&page_size=10
```

Headers:
```
Authorization: Bearer {token}
```

Parameters:
- `project_id`: Project ID
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)
- `start_date`: Filter by start date (optional)
- `end_date`: Filter by end date (optional)

### Bot Information

#### Get Bot Information

```
GET /dashapi/botinfo?project_id=your-project-id&page=1&page_size=10
```

Headers:
```
Authorization: Bearer {token}
```

## API Endpoints (for tracking)

### Log API Request

```
POST /api/log
```

Headers:
```
X-API-KEY: your-api-key
```

Request body:
```json
{
  "url": "https://your-api.com/endpoint",
  "method": "GET",
  "status_code": 200,
  "response_time": 0.125,
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

## Webhook Integrations

You can set up webhooks to receive notifications for certain events:

### Alert Webhook

```
POST /api/webhooks/alert
```

Headers:
```
X-API-KEY: your-api-key
```

Request body:
```json
{
  "alert_type": "server_error",
  "threshold": 10,
  "actual": 15,
  "project_id": "your-project-id",
  "timestamp": "2025-04-24T12:00:00Z"
}
```

## Error Codes

- `400`: Bad Request - Check request parameters
- `401`: Unauthorized - Invalid or expired token
- `403`: Forbidden - Valid token but insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `500`: Server Error - Something went wrong on the server

## Rate Limiting

The open source version does not include rate limiting, but you can implement it using standard FastAPI middleware.