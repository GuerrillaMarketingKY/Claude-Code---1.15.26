# ClickUp OAuth Setup Guide

This guide walks you through setting up OAuth 2.0 authentication for ClickUp Claude.

## 🔐 Why OAuth?

ClickUp uses OAuth 2.0 for secure authentication, not API tokens. OAuth provides:
- **Secure** - Tokens are encrypted and stored safely
- **Revocable** - You can revoke access anytime from ClickUp settings
- **Scoped** - Only access what's needed
- **Refresh** - Tokens automatically refresh when expired

---

## 📋 Step 1: Create a ClickUp OAuth App

1. **Log into ClickUp**
   - Go to your ClickUp workspace

2. **Navigate to Apps Settings**
   - Click your avatar (bottom left)
   - Go to **Settings** → **Apps**
   - Or visit directly: https://app.clickup.com/settings/apps

3. **Create New App**
   - Click **"Create an App"** or **"+ New App"**
   - Fill in the details:
     - **App Name**: `Claude Code Integration` (or your preferred name)
     - **Redirect URL**: `http://localhost:8089/callback`
     - **Description**: `Autonomous task execution with Claude Code`

4. **Save and Get Credentials**
   - After creating, you'll see:
     - **Client ID** - Copy this
     - **Client Secret** - Copy this (keep it secret!)

---

## 🔧 Step 2: Configure Environment Variables

### Option A: Export in Terminal (Temporary)

```bash
export CLICKUP_CLIENT_ID='your_client_id_here'
export CLICKUP_CLIENT_SECRET='your_client_secret_here'
```

These will only last for your current terminal session.

### Option B: Add to `.env` File (Permanent)

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
CLICKUP_CLIENT_ID=your_client_id_here
CLICKUP_CLIENT_SECRET=your_client_secret_here
```

3. Load the variables:
```bash
source .env
# or
export $(cat .env | xargs)
```

### Option C: Add to Shell Profile (Global)

Add to `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
export CLICKUP_CLIENT_ID='your_client_id_here'
export CLICKUP_CLIENT_SECRET='your_client_secret_here'
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

---

## 🔑 Step 3: Authenticate

Run the auth command:

```bash
./clickup-claude auth
```

**What happens:**

1. **Browser Opens** - A browser window opens to ClickUp OAuth page
2. **Authorize** - Click "Authorize" to grant access
3. **Redirect** - You'll be redirected to `localhost:8089/callback`
4. **Success** - See confirmation page and terminal message
5. **Token Stored** - OAuth token encrypted and saved to `~/.clickup-claude/`

**Example output:**
```
🔐 ClickUp OAuth Authentication
================================

📋 Step 1: Opening browser for authorization...
   URL: https://app.clickup.com/api?client_id=...

📋 Step 2: Waiting for authorization...
   (Please authorize the application in your browser)

✅ Authentication successful!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Access Token: AbC12345...XyZ98765
Expires At:   2026-01-16 23:45:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 You can now use 'clickup-claude execute <task-id>' to run tasks!
```

---

## ✅ Step 4: Test the Integration

Try executing a task:

```bash
./clickup-claude execute YOUR_TASK_ID
```

Or check a task status:

```bash
./clickup-claude status YOUR_TASK_ID
```

---

## 🔄 Token Management

### View Token Status

Tokens are stored in `~/.clickup-claude/tokens.enc` (encrypted).

### Logout (Clear Token)

```bash
./clickup-claude logout
```

This deletes your stored authentication. Run `auth` again to re-authenticate.

### Token Expiration

ClickUp OAuth tokens typically expire after 24 hours. When expired:
- You'll see an error: `"token expired"`
- Solution: Run `./clickup-claude auth` to get a new token

---

## 🔒 Security Features

### Encrypted Storage
- Tokens encrypted with AES-256-GCM
- Encryption key stored securely in `~/.clickup-claude/.key`
- File permissions: 0600 (only you can read)

### CSRF Protection
- Random state parameter prevents cross-site attacks
- State validated on OAuth callback

### Local Callback Server
- Runs only during authentication
- Listens on `localhost:8089` (not accessible externally)
- Auto-shuts down after receiving token

---

## 🛠️ Troubleshooting

### "CLICKUP_CLIENT_ID environment variable is required"

**Solution:** Make sure you've exported the environment variables:
```bash
export CLICKUP_CLIENT_ID='your_client_id'
export CLICKUP_CLIENT_SECRET='your_client_secret'
```

### "Browser didn't open automatically"

**Solution:** Manually copy the URL shown in terminal and open in browser.

### "Port 8089 already in use"

**Solution:**
1. Kill the process using port 8089:
```bash
lsof -ti:8089 | xargs kill -9
```

2. Or modify the callback URL in:
   - ClickUp app settings
   - `internal/auth/oauth.go` (CallbackURL constant)

### "Authorization failed: state mismatch"

**Solution:** This is a security error. Try again:
```bash
./clickup-claude logout
./clickup-claude auth
```

### "Token expired"

**Solution:** Re-authenticate:
```bash
./clickup-claude auth
```

### "API returned status 401"

**Solutions:**
1. Token might be invalid - re-authenticate
2. Check your OAuth app is still active in ClickUp settings
3. Verify Client ID and Secret are correct

---

## 📖 Next Steps

Once authenticated, you can:

1. **Execute Tasks Autonomously**
   ```bash
   ./clickup-claude execute TASK_ID
   ```

2. **Check Task Status**
   ```bash
   ./clickup-claude status TASK_ID
   ```

3. **Create ClickUp Tasks** with structured requirements
   - See `README.md` for task formatting guidelines

---

## 🔗 Useful Links

- **ClickUp API Documentation**: https://clickup.com/api
- **OAuth 2.0 Spec**: https://oauth.net/2/
- **ClickUp App Settings**: https://app.clickup.com/settings/apps

---

## 🆘 Need Help?

- Check the main `README.md` for usage examples
- See `DEMO.md` for a complete walkthrough
- Open an issue on GitHub

---

**Security Note:** Never share your Client Secret or access tokens. Keep them secure and rotate them regularly.
