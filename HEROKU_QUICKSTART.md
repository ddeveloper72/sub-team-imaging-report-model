# Heroku Deployment Quick Start

## Essential Config Vars for Heroku

Set these environment variables in your Heroku app dashboard or via CLI:

```bash
# Required for Flask
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set FLASK_ENV="production"
heroku config:set DEBUG="false"

# Optional for custom behavior
heroku config:set FLASK_RUN_HOST="0.0.0.0"
heroku config:set FLASK_RUN_PORT="5000"
```

## Important: Gunicorn vs Flask Development Server

**For Local Development (Windows):**
```bash
cd flask_app && python app.py
# Uses Flask development server (http://127.0.0.1:5000)
```

**For Production (Heroku/Linux):**
```bash
# Heroku automatically runs: gunicorn --bind 0.0.0.0:$PORT app:app
# Uses Gunicorn production server (much faster and more reliable)
```

**Note:** Gunicorn doesn't work on Windows - this is normal! Heroku's Linux servers run Gunicorn perfectly.

## Generate Your SECRET_KEY

Run this in your terminal to generate a secure secret key:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your SECRET_KEY.

## Deploy Commands

```bash
# Login to Heroku (if not already)
heroku login

# Create app (replace with your app name)
heroku create sub-team-imaging-report-model

# Set git remote
heroku git:remote -a sub-team-imaging-report-model

# Set config vars
heroku config:set SECRET_KEY="paste-your-generated-key-here"
heroku config:set FLASK_ENV="production"
heroku config:set DEBUG="false"

# Deploy
git push heroku main

# Open your app
heroku open
```

## Check Status

```bash
# View logs
heroku logs --tail

# Check config
heroku config

# Check app status
heroku ps
```

## Your app will be available at:
`https://sub-team-imaging-report-model.herokuapp.com`

## Files Already Configured:
- ✅ `Procfile` - Heroku process definition
- ✅ `requirements.txt` - Dependencies with gunicorn
- ✅ `flask_app/config.py` - Environment configuration
- ✅ `flask_app/app.py` - Production-ready Flask app
- ✅ `.gitignore` - Clean repository for deployment