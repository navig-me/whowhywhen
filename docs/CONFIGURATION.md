# WhoWhyWhen Configuration Guide

This document describes the available configuration options for WhoWhyWhen.

## Environment Variables

WhoWhyWhen uses environment variables for configuration. These can be set in a `.env` file in the root directory of the project.

### Database Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | None | Yes |

Example:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/whowhywhen
```

### Authentication

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | JWT signing key (min 32 chars) | None | Yes |
| `ALGORITHM` | JWT signing algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiry in minutes | 43200 (30 days) | No |

Example:
```
SECRET_KEY=your_very_secure_secret_key_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

### Google OAuth (Optional)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | None | Only for Google login |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | None | Only for Google login |
| `REDIRECT_URI` | OAuth callback URL | None | Only for Google login |

Example:
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8000/dashauth/oauth2callback
```

### Web Push Notifications (Optional)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VAPID_PRIVATE_KEY` | VAPID private key for web push | None | For push notifications |
| `VAPID_PUBLIC_KEY` | VAPID public key for web push | None | For push notifications |

Example:
```
VAPID_PRIVATE_KEY=your_vapid_private_key
VAPID_PUBLIC_KEY=your_vapid_public_key
```

You can generate VAPID keys using:
```bash
openssl ecparam -genkey -name prime256v1 -out vapid_private.pem
openssl ec -in vapid_private.pem -pubout -out vapid_public.pem
```

### Email Configuration (Optional)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_USERNAME` | SMTP username | None | For email notifications |
| `EMAIL_PASSWORD` | SMTP password | None | For email notifications |
| `EMAIL_SMTP_SERVER` | SMTP server hostname | None | For email notifications |
| `EMAIL_SMTP_PORT` | SMTP server port | 587 | No |
| `EMAIL_IMAP_SERVER` | IMAP server hostname | None | For email fetching |
| `EMAIL_IMAP_PORT` | IMAP server port | 993 | No |
| `ADMIN_EMAIL` | Email for admin notifications | admin@example.com | No |

Example:
```
EMAIL_USERNAME=noreply@example.com
EMAIL_PASSWORD=your_secure_password
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=imap.example.com
EMAIL_IMAP_PORT=993
ADMIN_EMAIL=admin@example.com
```

## Frontend Configuration

Frontend configuration is stored in `who-why-when-landing-page/src/config.js`.

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | URL of the API server | http://localhost:8001 |
| `DASH_API_BASE_URL` | URL of the dashboard API | http://localhost:8000 |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | From environment |

## Advanced Configuration

### Database Migrations

Database migrations are managed by Alembic. The configuration is in `alembic.ini`.

### Docker Configuration

Docker configuration is in `docker-compose.yml` and the individual Dockerfiles.

You can customize ports, volumes, and other Docker settings by editing these files.

### Logging

Logging configuration is handled through the standard Python logging module. You can customize logging by modifying the logger configuration in the application.

## Troubleshooting

### Database Connection Issues

If you're having trouble connecting to the database:

1. Verify that PostgreSQL is running
2. Check that the `DATABASE_URL` in your `.env` file is correct
3. Ensure your database user has the necessary permissions

### Email Sending Issues

If emails aren't being sent:

1. Check your SMTP credentials
2. Verify that your email provider allows application access
3. Try enabling "less secure apps" if using Gmail

### OAuth Configuration

For Google OAuth:

1. Create a project in the Google Developer Console
2. Configure OAuth consent screen
3. Create OAuth credentials (Web application type)
4. Add authorized redirect URIs that match your `REDIRECT_URI`