# 🔵 Azure OpenAI Setup Guide

Complete guide to set up Azure OpenAI for the GenAI Live Environment Assistant

---

## 📋 Prerequisites

- Azure account with active subscription
- Azure OpenAI access (you mentioned you have free credits ✅)

---

## 🚀 Step-by-Step Setup in Azure Portal

### Step 1: Create Azure OpenAI Resource

1. **Go to Azure Portal**: https://portal.azure.com

2. **Search for "Azure OpenAI"** in the top search bar

3. **Click "Create"** or **"+ Create"**

4. **Fill in the details**:

   ```
   Subscription: [Your Subscription]
   Resource Group: [Create new or select existing]
   Region: East US, West Europe, or your preferred region
   Name: [Your unique name, e.g., "my-genai-assistant"]
   Pricing Tier: Standard S0 (or your available tier)
   ```

5. **Click "Review + Create"** → **"Create"**

6. **Wait 2-3 minutes** for deployment to complete

---

### Step 2: Deploy GPT-4 Model

1. **Open your Azure OpenAI resource** (from the deployment notification or resource list)

2. **Click "Go to Azure OpenAI Studio"** button

   - Or visit: https://oai.azure.com/

3. **Navigate to "Deployments"** (left sidebar)

4. **Click "Create new deployment"** or **"+ Create"**

5. **Configure deployment**:

   ```
   Model: gpt-4 (or gpt-4-turbo if available)
   Deployment name: gpt-4
   Model version: Latest or specific version
   Deployment type: Standard
   Tokens per minute rate limit: 10K (or as per your quota)
   ```

6. **Click "Create"**

7. **Note your deployment name** (e.g., "gpt-4") - you'll need this!

---

### Step 3: Get Your Credentials

#### A. Get API Key

1. In **Azure Portal**, go to your **Azure OpenAI resource**

2. Click **"Keys and Endpoint"** (left sidebar under Resource Management)

3. **Copy KEY 1** (or KEY 2)
   ```
   Example: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
   ```

#### B. Get Endpoint URL

1. Same page as above (**Keys and Endpoint**)

2. **Copy the Endpoint URL**

   ```
   Example: https://my-genai-assistant.openai.azure.com/
   ```

   ⚠️ **Important**: Must end with `/`

#### C. Get API Version

Use the latest stable version:

```
2024-02-15-preview
```

Or check: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference

---

## 🔧 Configure the Application

### Option 1: Using .env File (Recommended)

1. **Navigate to project directory**:

   ```bash
   cd /Users/abhaygupta/Desktop/GenAI-Powered-Live-Environment-Assistant
   ```

2. **Edit the .env file**:

   ```bash
   nano .env
   ```

   Or if .env doesn't exist:

   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Add your Azure credentials**:

   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
   AZURE_OPENAI_ENDPOINT=https://my-genai-assistant.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Application Settings
   APP_TITLE=GenAI Live Environment Assistant
   LOG_LEVEL=INFO
   ```

4. **Save and exit**:
   - Press `Ctrl+X`
   - Press `Y`
   - Press `Enter`

### Option 2: Using the UI (Alternative)

When you run the app, enter credentials in the sidebar:

- API Key
- Endpoint
- Deployment Name

---

## ✅ Verification

### Test Your Configuration

1. **Run the application**:

   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

2. **Check if credentials load**:

   - Open browser at http://localhost:8501
   - Sidebar should show your endpoint (if using .env)
   - Or enter manually in the sidebar

3. **Test analysis**:
   - Select a scenario
   - Click "Analyze Error"
   - Should see AI analysis within 5-10 seconds

---

## 🎯 Quick Reference Card

Save this for quick access:

```
┌─────────────────────────────────────────────────┐
│ YOUR AZURE OPENAI CREDENTIALS                   │
├─────────────────────────────────────────────────┤
│                                                 │
│ API Key:                                        │
│ [Paste from Azure Portal > Keys and Endpoint]  │
│                                                 │
│ Endpoint:                                       │
│ https://[your-resource].openai.azure.com/      │
│                                                 │
│ Deployment Name:                                │
│ gpt-4 (or what you named your deployment)      │
│                                                 │
│ API Version:                                    │
│ 2024-02-15-preview                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Error: "Resource not found"

**Problem**: Wrong endpoint or deployment name

**Solution**:

1. Check endpoint in Azure Portal > Keys and Endpoint
2. Verify deployment name in Azure OpenAI Studio > Deployments
3. Ensure endpoint ends with `/`

### Error: "Access denied" or "401 Unauthorized"

**Problem**: Wrong API key

**Solution**:

1. Go to Azure Portal > Your Resource > Keys and Endpoint
2. Copy KEY 1 again (ensure no spaces)
3. Update .env file

### Error: "Deployment not found"

**Problem**: Deployment name doesn't match

**Solution**:

1. Go to https://oai.azure.com/
2. Click "Deployments"
3. Check exact name of your GPT-4 deployment
4. Update AZURE_OPENAI_DEPLOYMENT_NAME in .env

### Error: "Rate limit exceeded"

**Problem**: Too many requests

**Solution**:

1. Wait a few seconds and try again
2. Check your quota in Azure OpenAI Studio
3. Increase tokens per minute limit in deployment settings

### Error: "API version not supported"

**Problem**: Old or wrong API version

**Solution**:
Update to latest version:

```env
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

---

## 💰 Cost Management

### How Much Will This Cost?

Azure OpenAI pricing (as of Oct 2024):

- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **Per analysis**: ~$0.02-0.05 (depending on log size)

### Your Free Credits

If you have free credits:

- Track usage in Azure Portal > Cost Management
- Set up budget alerts
- Monitor in Azure OpenAI Studio > Quotas

### Tips to Save Credits:

1. **Use smaller context**: Only analyze relevant log sections
2. **Lower temperature**: Already set to 0.2 for consistency
3. **Test with one scenario first**: Before running all scenarios
4. **Cache results**: Save analysis results locally

---

## 📊 Monitor Your Usage

### In Azure Portal:

1. Go to your **Azure OpenAI resource**
2. Click **"Metrics"** (left sidebar)
3. Add metric: **"Total Tokens"**
4. View your usage over time

### In Azure OpenAI Studio:

1. Go to https://oai.azure.com/
2. Click **"Quotas"** (top right)
3. See your rate limits and usage

---

## 🔐 Security Best Practices

1. **Never commit .env to Git**

   - Already in .gitignore ✅

2. **Regenerate keys if exposed**

   - Azure Portal > Keys and Endpoint > Regenerate

3. **Use different keys for dev/prod**

   - Create separate deployments

4. **Set up budget alerts**
   - Azure Portal > Cost Management > Budgets

---

## 🎓 Additional Resources

- **Azure OpenAI Documentation**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **API Reference**: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference
- **Pricing**: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/
- **Quota Management**: https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits

---

## ✅ Checklist

Before running the app, verify:

- [ ] Azure OpenAI resource created
- [ ] GPT-4 model deployed
- [ ] API Key copied
- [ ] Endpoint URL copied (with trailing `/`)
- [ ] Deployment name noted
- [ ] .env file updated with all credentials
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] App starts without errors: `streamlit run app.py`

---

## 🆘 Need Help?

### Common Issues:

**Can't find Azure OpenAI in portal?**

- Search for "Azure OpenAI" or "Cognitive Services"
- You may need to request access first

**Don't have GPT-4 access?**

- Try GPT-3.5-turbo (works but less accurate)
- Request GPT-4 access via Azure OpenAI Studio

**Free credits not showing?**

- Check your subscription in Azure Portal
- Verify you have an active sponsorship or trial

---

## 🎉 You're All Set!

Once you've completed the setup:

1. Your credentials are in `.env`
2. Dependencies are installed
3. Run: `./run.sh` or `streamlit run app.py`
4. Start analyzing errors! 🚀

---

**Next**: Check out `QUICKSTART.md` for usage guide!
