# WhoWhyWhen Setup Guide

This guide provides step-by-step instructions for setting up WhoWhyWhen in different environments.

## Local Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/whowhywhen.git
   cd whowhywhen
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to match your setup.

5. **Set up PostgreSQL**:
   - Create a database for the application
   - Update the `DATABASE_URL` in your `.env` file

6. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start the servers**:
   ```bash
   # API server
   uvicorn app.main_api:app --reload --port 8001
   
   # Dashboard server
   uvicorn app.main_dash:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd who-why-when-landing-page
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Docker Setup

For a simplified setup, you can use Docker and Docker Compose:

1. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to match your setup.

2. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

3. **Run migrations**:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

4. **Access the application**:
   - API: http://localhost:8001
   - Dashboard: http://localhost:8000
   - Landing page: http://localhost:5000

## Security Considerations

1. **API Keys**: Generate strong API keys for production use.
2. **JWT Secret**: Use a strong random key for JWT token generation.
3. **Environment Variables**: Keep your `.env` file secure and never commit it to version control.
4. **Database**: Use a secure password for your database and restrict network access.

## Common Issues and Solutions

### Database Connection Issues
- Check that PostgreSQL is running
- Verify that the database credentials in `.env` are correct
- Ensure the database exists

### Email Configuration
- If emails are not being sent, check SMTP settings in `.env`
- Some email providers require specific security settings

### Frontend Connection Issues
- Verify API URL in `config.js` points to the correct backend URL
- Check for CORS issues if using different domains

## Next Steps

After installation:

1. **Create a user account:**
   - Navigate to http://localhost:8000 in your browser
   - Click "Register" and fill out the form
   - Verify your email if email verification is configured

2. **Create a project:**
   - In the dashboard, click the "Projects" section
   - Click "New Project" and provide a name
   - This will be used to organize your API endpoints

3. **Generate an API key:**
   - Select your project from the dashboard
   - Go to "API Keys" section
   - Click "Generate New Key"
   - Save the key securely - it will only be shown once

4. **Integrate the tracking middleware:**
   - Follow the integration guide for your framework
   - Use the API key you generated
   - Point to your WhoWhyWhen instance

5. **Start monitoring your API traffic:**
   - Make a few requests to your API
   - Return to the dashboard to see the analytics
   - Set up alerts for critical issues

## Upgrading

To upgrade WhoWhyWhen to a newer version:

### Docker Installation

```bash
# Pull the latest changes
git pull origin main

# Rebuild containers with new code
docker-compose build

# Apply any database migrations
docker-compose run api alembic upgrade head

# Restart the services
docker-compose down
docker-compose up -d
```

### Manual Installation

```bash
# Pull the latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Restart the services
# (This depends on how you're running the services)
```

## Troubleshooting

### Common Issues

- **"No module named 'xyz'"**: Run `pip install -r requirements.txt` to install missing dependencies
- **Database connection errors**: Check your .env file and ensure PostgreSQL is running
- **"Table doesn't exist"**: Run `alembic upgrade head` to apply migrations
- **CORS errors**: Check that your frontend URLs are allowed in the CORS configuration

### Getting Help

If you're stuck, you can:

- Check the [GitHub issues](https://github.com/navig-me/whowhywhen/issues) for similar problems
- Open a new issue with details about your problem
- Contribute improvements to the documentation to help others