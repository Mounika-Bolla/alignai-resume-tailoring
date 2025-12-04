# 🔐 Social Login Setup Guide

## 🎯 **What We Built:**

Your AlignAI app now supports **Social Login** with:
- ✅ Google
- ✅ LinkedIn  
- ✅ GitHub

Users can sign up / log in with one click!

---

## ⚡ **Quick Test (Without OAuth Setup)**

Even without OAuth credentials, you can test the system:

1. **Start servers:** `START_SERVERS.bat`
2. **Open:** http://localhost:8000/login.html
3. **Click a social login button** (Google, LinkedIn, GitHub)
4. **You'll see:** "OAuth not configured" message

**This is normal! You need to set up OAuth credentials first.**

---

## 🔧 **How Social Login Works**

```
┌─────────────────────────────────────────────┐
│  1. User clicks "Login with Google"         │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  2. Redirect to Google's login page         │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  3. User logs in with Google account        │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  4. Google redirects back to AlignAI        │
│     with authorization code                 │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  5. AlignAI exchanges code for user info    │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  6. Create account or login existing user   │
└───────────────┬─────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  7. User logged in → Dashboard ✅            │
└─────────────────────────────────────────────┘
```

---

## 📋 **Setup Instructions**

### **Option 1: Skip OAuth Setup (For Now)**

If you want to test other features first:

✅ **Just use email login/signup!**

The social login buttons will show "not configured" messages, but the rest of your app works perfectly!

---

### **Option 2: Set Up OAuth (Full Social Login)**

Follow these guides to enable each provider:

---

## 🔵 **Google OAuth Setup**

### **Step 1: Create Google Cloud Project**

1. **Go to:** https://console.cloud.google.com/
2. **Click:** "Select a project" → "New Project"
3. **Name:** AlignAI
4. **Click:** "Create"

### **Step 2: Enable Google+ API**

1. **Go to:** "APIs & Services" → "Library"
2. **Search:** "Google+ API"
3. **Click:** "Enable"

### **Step 3: Create OAuth Credentials**

1. **Go to:** "APIs & Services" → "Credentials"
2. **Click:** "Create Credentials" → "OAuth client ID"
3. **Click:** "Configure Consent Screen"
   - **User Type:** External
   - **App name:** AlignAI
   - **User support email:** Your email
   - **Developer email:** Your email
   - **Click:** "Save and Continue"
   - **Scopes:** Just click "Save and Continue" (default is fine)
   - **Test users:** Add your email
   - **Click:** "Save and Continue"
4. **Back to Create OAuth Client ID:**
   - **Application type:** Web application
   - **Name:** AlignAI Web Client
   - **Authorized redirect URIs:** 
     ```
     http://localhost:5000/api/auth/callback/google
     ```
   - **Click:** "Create"

### **Step 4: Get Credentials**

You'll see:
- **Client ID:** (long string)
- **Client Secret:** (another long string)

**Save these!** You'll need them.

### **Step 5: Add to `.env` File**

Create/edit `.env` file in your project:

```env
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

---

## 🔵 **LinkedIn OAuth Setup**

### **Step 1: Create LinkedIn App**

1. **Go to:** https://www.linkedin.com/developers/apps
2. **Click:** "Create app"
3. **Fill in:**
   - **App name:** AlignAI
   - **LinkedIn Page:** (Create a company page or use personal)
   - **App logo:** Upload your logo
   - **Privacy policy URL:** (temporary: use https://example.com)
   - **Legal agreement:** Check box
4. **Click:** "Create app"

### **Step 2: Get Credentials**

1. **Go to:** "Auth" tab
2. **Copy:**
   - **Client ID**
   - **Client Secret**

### **Step 3: Add Redirect URL**

1. **Scroll to:** "OAuth 2.0 settings"
2. **Redirect URLs:** Add:
   ```
   http://localhost:5000/api/auth/callback/linkedin
   ```
3. **Click:** "Update"

### **Step 4: Request Access**

1. **Go to:** "Products" tab
2. **Find:** "Sign In with LinkedIn using OpenID Connect"
3. **Click:** "Request access"
4. **Wait for approval** (usually instant)

### **Step 5: Add to `.env` File**

```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
```

---

## ⚫ **GitHub OAuth Setup**

### **Step 1: Create OAuth App**

1. **Go to:** https://github.com/settings/developers
2. **Click:** "OAuth Apps" → "New OAuth App"
3. **Fill in:**
   - **Application name:** AlignAI
   - **Homepage URL:** `http://localhost:8000`
   - **Authorization callback URL:**
     ```
     http://localhost:5000/api/auth/callback/github
     ```
4. **Click:** "Register application"

### **Step 2: Generate Client Secret**

1. **Click:** "Generate a new client secret"
2. **Copy the secret** (it's shown only once!)

### **Step 3: Get Client ID**

**Copy the Client ID** shown at the top

### **Step 4: Add to `.env` File**

```env
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
```

---

## 📄 **Complete `.env` File Example**

Create a file named `.env` in your project root:

```env
# PostgreSQL (you already have this)
POSTGRES_PASSWORD=postgres

# Google OAuth
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefg123456

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=abc123def456
LINKEDIN_CLIENT_SECRET=xyz789uvw012

# GitHub OAuth
GITHUB_CLIENT_ID=Iv1.a1b2c3d4e5f6g7h8
GITHUB_CLIENT_SECRET=1234567890abcdef1234567890abcdef12345678
```

**⚠️ IMPORTANT:** 
- Never commit `.env` to Git!
- Add `.env` to `.gitignore`

---

## 🧪 **Testing Social Login**

### **Step 1: Install Requirements**

```bash
pip install requests
```

### **Step 2: Restart Backend**

```bash
# Stop the current backend (Ctrl+C in terminal)
# Start it again:
python auth.py
```

### **Step 3: Test**

1. **Open:** http://localhost:8000/login.html
2. **Click:** "Continue with Google" (or LinkedIn/GitHub)
3. **You should be redirected** to the provider's login page
4. **Login** with your account
5. **You'll be redirected back** to your dashboard
6. **Success!** ✅

---

## 🔍 **Troubleshooting**

### **Problem: "OAuth not configured"**

**Solutions:**
- ✅ Check `.env` file exists in project root
- ✅ Check credentials are correct (no extra spaces)
- ✅ Restart backend server after adding credentials
- ✅ Make sure `python-dotenv` is installed

**Test:**
```bash
python -c "from oauth_config import is_provider_configured; print('Google:', is_provider_configured('google'))"
```

Should show: `Google: True`

---

### **Problem: "Redirect URI mismatch"**

**Solution:**

Make sure redirect URI in provider settings **exactly matches**:
- Google: `http://localhost:5000/api/auth/callback/google`
- LinkedIn: `http://localhost:5000/api/auth/callback/linkedin`
- GitHub: `http://localhost:5000/api/auth/callback/github`

**⚠️ No trailing slash! Must be exact!**

---

### **Problem: "User email not available"**

**Solutions:**

**Google:**
- Make sure "Google+ API" is enabled
- Check OAuth consent screen includes email scope

**GitHub:**
- User's email must be public, or
- App needs `user:email` scope (already included)

**LinkedIn:**
- Make sure "Sign In with LinkedIn using OpenID Connect" product is approved

---

### **Problem: "Invalid client"**

**Solutions:**
- Double-check Client ID and Secret
- Make sure no extra spaces in `.env`
- Verify credentials are for the correct app/environment

---

## 📊 **How It Works in Your Code**

### **Backend Routes (auth.py):**

1. **`/api/auth/oauth/<provider>`**
   - Generates OAuth authorization URL
   - Redirects user to provider

2. **`/api/auth/callback/<provider>`**
   - Handles callback from provider
   - Exchanges code for access token
   - Gets user info
   - Creates account or logs in existing user
   - Redirects to dashboard

3. **`/api/auth/providers`**
   - Returns which providers are configured

### **Frontend (login.html):**

```javascript
async function socialLogin(provider) {
    // 1. Get authorization URL from backend
    const response = await fetch(`${API_URL}/auth/oauth/${provider}`);
    const data = await response.json();
    
    // 2. Redirect user to provider's login
    window.location.href = data.auth_url;
}
```

### **Configuration (oauth_config.py):**

```python
OAUTH_PROVIDERS = {
    'google': {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
        ...
    }
}
```

---

## 🎯 **User Flow Example**

```
1. User clicks "Login with Google"
   ↓
2. JavaScript calls: /api/auth/oauth/google
   ↓
3. Backend returns Google's auth URL
   ↓
4. Browser redirects to: accounts.google.com/...
   ↓
5. User logs in with Google
   ↓
6. Google redirects to: localhost:5000/api/auth/callback/google?code=ABC...
   ↓
7. Backend exchanges code for token
   ↓
8. Backend gets user email and name
   ↓
9. Backend checks if user exists:
   - If yes: Login existing user
   - If no: Create new account
   ↓
10. Backend creates session
   ↓
11. Backend redirects to: localhost:8000/dashboard.html
   ↓
12. User sees dashboard with their name ✅
```

---

## ✅ **Success Checklist**

- [ ] Created OAuth apps for each provider
- [ ] Got Client ID and Client Secret for each
- [ ] Added credentials to `.env` file
- [ ] Installed `requests` library
- [ ] Restarted backend server
- [ ] Tested Google login → Success!
- [ ] Tested LinkedIn login → Success!
- [ ] Tested GitHub login → Success!

---

## 🚀 **Production Deployment**

When deploying to production:

### **1. Update Redirect URIs**

Change from:
```
http://localhost:5000/api/auth/callback/google
```

To:
```
https://yourdomain.com/api/auth/callback/google
```

### **2. Update oauth_config.py**

```python
# Use environment variable for domain
DOMAIN = os.getenv('DOMAIN', 'http://localhost:5000')

'redirect_uri': f'{DOMAIN}/api/auth/callback/google'
```

### **3. Environment Variables**

Set these on your hosting platform:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `LINKEDIN_CLIENT_ID`
- `LINKEDIN_CLIENT_SECRET`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `DOMAIN`

---

## 📚 **Additional Resources**

- **Google OAuth:** https://developers.google.com/identity/protocols/oauth2
- **LinkedIn OAuth:** https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication
- **GitHub OAuth:** https://docs.github.com/en/apps/oauth-apps/building-oauth-apps

---

## 💡 **Pro Tips**

1. **Start with one provider** (Google is easiest)
2. **Test in incognito mode** to see fresh user experience
3. **Check console logs** if something fails
4. **User email must be available** from provider
5. **OAuth credentials are free!** No payment needed for basic usage

---

## 🎉 **You're Done!**

Social login is now fully functional! Users can:
- ✅ Click "Continue with Google/LinkedIn/GitHub"
- ✅ Login with their existing account
- ✅ No password needed!
- ✅ Instant access to dashboard

**Happy coding!** 🚀✨

