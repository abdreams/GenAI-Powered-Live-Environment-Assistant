# 🚀 POC Demo Guide - GenAI Live Environment Assistant

## Overview
This is an enterprise-grade POC showcasing AI-powered production monitoring and root cause analysis for banking/payment systems.

## 🎯 Key Features Demonstrated

### 1. **💬 AI Assistant Tab** (Main Demo Focus)
- **Conversational Interface**: Ask natural language questions about production issues
- **Sample Questions to Demo**:
  - "What's causing the high error rate in payment service?"
  - "Analyze the recent database connection issues"
  - "Show me the root cause of transaction failures"
  - "Why are we seeing deadlock errors?"
  - "What's causing the connection pool exhaustion?"

### 2. **📊 Live Dashboard Tab**
- **Real-time Anomaly Detection**: Shows 20+ anomalies detected automatically
- **System Metrics**: Live health indicators
- **Service Status**: Multi-service health monitoring
- **Integration Status**: Shows connected data sources

### 3. **🔍 Deep Dive Analysis Tab**
- Transaction flow analysis
- Database performance deep dive
- Error pattern recognition
- Capacity planning

## 🎨 Visual Highlights

### Top Metrics Bar
- System Health: 92%
- Active Alerts: 7
- Avg Response Time: 245ms
- Uptime: 99.8%

### Sidebar Integrations (Mock - For Demo)
- ✅ **AppDynamics** - Connected (APM monitoring)
- ✅ **Splunk** - Connected (Log aggregation)
- ✅ **SQL Server** - Connected (Database logs)
- ✅ **GitHub** - Connected (Code repository)
- 🟡 **Prometheus** - Standby (Metrics)
- 🟡 **Datadog** - Standby (Monitoring)

### Service Health Status
- 🟡 **Payment Service**: Degraded (98.2% uptime, 12 errors)
- 🔴 **Database Service**: Critical (99.1% uptime, 8 errors)
- 🟢 **Auth Service**: Healthy (99.9% uptime, 0 errors)
- 🟢 **Notification Service**: Healthy (99.8% uptime, 1 error)

## 📋 Demo Script

### Step 1: Show Dashboard (15 seconds)
1. Open the app → Navigate to **"Live Dashboard"** tab
2. Point out real-time anomaly detection showing 20+ issues
3. Highlight service health status showing degraded/critical services

### Step 2: Show Integrations (10 seconds)
1. Point to sidebar showing connected data sources
2. Mention: "Connects to AppDynamics, Splunk, SQL Server, etc."

### Step 3: AI Assistant Demo (2-3 minutes)
1. Go to **"Ask AI Assistant"** tab
2. Type in text area: *"What's causing the database connection pool exhaustion?"*
3. Click **"🚀 Analyze"**
4. Show AI analyzing logs, metrics, and code
5. Point out results:
   - **Error Logs**: Shows actual error traces
   - **Anomalies**: 20 detected issues with severity levels
   - **Code Context**: Maps errors to specific code lines
   - **AI Analysis**: 
     - Root cause identified
     - Impact assessment
     - Technical details
     - Immediate fix recommendations
     - Prevention strategies
     - Monitoring recommendations

### Step 4: Show Code Mapping (30 seconds)
1. Expand code context sections
2. Show how errors are mapped to:
   - `database_manager.py` line 91 (lock timeout)
   - `transaction_handler.py` line 49 (transfer failure)
   - `payment_service.py` line 44 (processing error)

### Step 5: Q&A Examples
**Q**: "How does it know which code caused the issue?"
**A**: "AI parses stack traces from logs and maps them to the actual codebase, showing exact file, function, and line numbers"

**Q**: "Can this work with our existing tools?"
**A**: "Yes! It's designed to integrate with AppDynamics, Splunk, Datadog, etc. (show sidebar integrations)"

**Q**: "What kind of issues can it detect?"
**A**: "Deadlocks, connection pool exhaustion, lock timeouts, slow queries, memory leaks, and patterns across logs and metrics"

## 🎯 Value Proposition Talking Points

1. **Reduces MTTR** (Mean Time To Resolution)
   - From hours → minutes
   - AI analyzes 1000s of log lines instantly

2. **Proactive Detection**
   - Catches issues before customers notice
   - Live dashboard with 20+ anomalies detected

3. **Root Cause, Not Just Symptoms**
   - Maps errors to exact code locations
   - Provides fix recommendations

4. **Enterprise Integrations**
   - Works with existing tools (AppD, Splunk, SQL)
   - No replacement needed

5. **Banking-Grade Accuracy**
   - Understands financial transactions
   - Detects deadlocks, race conditions, etc.

## 🔧 Technical Setup (For Demo)

### Azure OpenAI Configuration
- Collapse the "Azure OpenAI Settings" in sidebar (already configured via .env)
- Or configure live during demo for transparency

### Sample Queries for Different Scenarios
```
1. "Analyze the payment service errors"
2. "Why are database transactions failing?"
3. "What's causing the lock timeout issues?"
4. "Show me the connection pool problems"
5. "Investigate the recent spike in errors"
```

## 📊 Key Metrics Shown

- **20+ Anomalies Detected** (mix of critical, high, medium)
- **16 Code Contexts Mapped** (exact error locations)
- **4 Services Monitored** (Payment, Database, Auth, Notification)
- **6 Integration Points** (AppDynamics, Splunk, SQL, GitHub, Prometheus, Datadog)

## 🎬 Demo Duration
- **Quick Demo**: 2-3 minutes (Dashboard + One AI query)
- **Full Demo**: 5-7 minutes (All features + Code mapping)
- **Deep Dive**: 10-15 minutes (With Q&A and technical discussion)

## 💡 Tips for Demo Success

1. **Start with Dashboard**: Shows immediate value
2. **Use Conversational Query**: Makes it feel natural
3. **Show Code Mapping**: Most impressive technical feature
4. **Highlight Integrations**: Shows enterprise readiness
5. **End with ROI**: Time saved, faster resolution

## 🚨 Known Limitations (For Transparency)

- This is a POC with dummy banking data
- Integrations are UI-only (not functionally connected yet)
- Designed to showcase AI capabilities with realistic scenarios

---

**Built with**: Streamlit, LangChain, Azure OpenAI GPT-4, Python
**Focus**: Banking/Payment Systems Production Monitoring
**Target**: 10-hour POC for enterprise demonstration
