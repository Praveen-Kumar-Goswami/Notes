# Deploying to Render

## Step 1: Prepare Firebase Credentials

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download the JSON file
4. Copy the entire contents of the JSON file

## Step 2: Create Render Account

1. Go to [render.com](https://render.com) and sign up/login
2. Connect your GitHub account (or use GitLab/Bitbucket)

## Step 3: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure the service:
   - **Name**: make-a-note (or any name you prefer)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free or Starter (your choice)

## Step 4: Set Environment Variables

In the Render dashboard, go to your service → Environment tab and add:

1. **SECRET_KEY**: 
   - Generate a random secret key (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - Add it as an environment variable

2. **FIREBASE_CREDENTIALS**:
   - Paste the entire JSON content from Step 1
   - Make sure to paste it as a single line or use Render's JSON editor
   - Example format (all on one line):
   ```
   {"type":"service_account","project_id":"your-project-id",...}
   ```

## Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Wait for the build to complete
4. Your app will be available at: `https://your-app-name.onrender.com`

## Step 6: Update Firebase Authorized Domains

1. Go to Firebase Console → Authentication → Settings → Authorized domains
2. Add your Render domain: `your-app-name.onrender.com`

## Important Notes

- The first deployment may take a few minutes
- Free tier services spin down after 15 minutes of inactivity
- Make sure `firebase-config.json` is in `.gitignore` (already added)
- Your Firebase web config in `static/js/firebase-config.js` should already be set up

## Troubleshooting

- If build fails, check the build logs in Render dashboard
- If Firebase auth doesn't work, verify authorized domains in Firebase Console
- If you see 500 errors, check the service logs in Render dashboard

