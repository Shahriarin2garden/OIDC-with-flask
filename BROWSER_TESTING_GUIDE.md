# OIDC Provider Browser Testing Guide

## 🚨 CRITICAL: Browser Setup for Testing

### Step 1: Clear All Browser Data
**Chrome:**
1. Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
2. Select "All time" 
3. Check all boxes: Cookies, Cache, Local Storage, etc.
4. Click "Clear data"

**Firefox:**
1. Press `Ctrl+Shift+Delete`
2. Select "Everything"
3. Check all boxes
4. Click "Clear Now"

### Step 2: Use Incognito/Private Mode
- **Chrome**: `Ctrl+Shift+N`
- **Firefox**: `Ctrl+Shift+P`
- **Edge**: `Ctrl+Shift+N`

### Step 3: Disable Extensions
1. Go to browser settings
2. Disable all extensions temporarily
3. Restart browser

## 🔑 Test Credentials

| Username | Password     |
|----------|-------------|
| alice    | alicepassword |
| bob      | bobpassword   |

## 🧪 Manual Testing Steps

### Option A: Run Enhanced Test Client
```bash
python test_client_enhanced.py
```

### Option B: Manual URL Testing
1. Copy this URL into your browser:
```
http://localhost:5000/authorize?response_type=code&client_id=client123&redirect_uri=http://localhost:8080/callback&scope=openid%20profile%20email&code_challenge=test123&code_challenge_method=S256
```

2. Login with: `alice` / `alicepassword`
3. Grant consent when prompted

## 🐛 Troubleshooting Common Issues

### Issue: "invalid_credentials" Error
**Solutions:**
1. ✅ Clear browser data completely
2. ✅ Use fresh incognito window  
3. ✅ Try different browser
4. ✅ Check for typos in username/password
5. ✅ Ensure no extra spaces before/after credentials

### Issue: Form Doesn't Submit
**Solutions:**
1. ✅ Enable JavaScript
2. ✅ Disable ad blockers
3. ✅ Check browser console for errors (F12)
4. ✅ Try pressing Enter instead of clicking button

### Issue: Page Keeps Refreshing
**Solutions:**
1. ✅ Close all localhost tabs
2. ✅ Restart browser
3. ✅ Use different port (if port 8080 is busy)

### Issue: Multiple Sessions Conflict
**Solutions:**
1. ✅ Use only one browser tab
2. ✅ Clear sessions: Delete cookies for localhost
3. ✅ Restart the Flask server

## 🔍 Debug Steps

### Check Server Logs
The Flask server shows detailed logs. Look for:
```
Login attempt for user: alice
Found user: {'sub': 'user-alice', ...}
User alice authenticated successfully
```

### Check Browser Network Tab
1. Press F12 → Network tab
2. Submit login form
3. Check if POST request is made to `/authorize`
4. Check response status and content

### Verify Form Data
In browser console (F12), type:
```javascript
// Check if form fields exist
document.querySelector('input[name="username"]').value
document.querySelector('input[name="password"]').value
```

## ✅ Expected Flow

1. **Authorization Request** → Login page appears
2. **Login Submission** → Consent page appears  
3. **Consent Granted** → Redirect to callback with authorization code
4. **Token Exchange** → Access token and ID token received
5. **User Info** → User profile information retrieved

## 🎯 Success Indicators

- ✅ Server logs show successful authentication
- ✅ Consent page appears after login
- ✅ Callback URL receives authorization code
- ✅ Tokens are successfully exchanged
- ✅ User information is retrieved

If you still experience issues after following this guide, the problem may be in the form submission mechanism or browser-specific behavior.
