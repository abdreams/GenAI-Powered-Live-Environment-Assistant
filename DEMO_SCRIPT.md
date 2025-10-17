# Demo Script for Presentation

## Introduction (1 minute)

"Hello! Today I'll demonstrate our GenAI-Powered Live Environment Assistant - a tool that helps DevOps teams quickly identify and fix production issues by automatically mapping error logs to code and providing AI-powered analysis."

## The Problem (1 minute)

"In production environments, especially in banking systems:

- Errors happen in logs
- Stack traces span multiple files
- Finding the root cause takes hours
- Understanding the impact is crucial
- We need to fix it FAST

Traditional approach: Manual log searching, reading code, correlating events. Time-consuming!"

## Our Solution (8 minutes)

### Scenario 1: Database Deadlock (3 minutes)

**Setup:**

1. Open the application
2. Select "Scenario 1: SQL Lock Timeout & Deadlock"
3. Click "Analyze Error"

**Demonstrate:**

- Point out the error logs on the left
- Show the stack trace
- **Highlight the code mapping** - "See how it automatically identified the exact line causing the issue?"
- Show the AI analysis explaining the deadlock
- Point out the root cause, impact, and fix recommendations

**Key Points:**

- "The system detected a deadlock between two transactions"
- "It identified the exact function: `execute_transaction` at line 91"
- "AI explains WHY it happened - two transactions waiting for each other's locks"
- "Provides immediate fix: adjust isolation level or implement retry logic"

### Scenario 2: Connection Pool Exhaustion (3 minutes)

**Setup:**

1. Select "Scenario 2: Connection Pool Exhaustion"
2. Click "Analyze Error"

**Demonstrate:**

- Show the anomaly detection - "10/10 connections in use"
- Point out the metrics showing degradation
- Show how AI mapped it to `get_connection` method
- Discuss the business impact: "Failed payments = lost revenue"

**Key Points:**

- "System detected connection pool at 100%"
- "Anomaly detector flagged this BEFORE it became critical"
- "AI recommends: increase pool size, implement connection timeouts, add circuit breakers"

### Scenario 3: Combined Analysis (2 minutes)

**Quick demo showing multiple issues:**

- Multiple anomalies detected
- Timeline of events
- Cascading failures
- Comprehensive analysis

## Architecture Overview (2 minutes)

Show the tech stack:

- **Streamlit**: Interactive UI
- **LangChain + GPT-4**: Intelligent analysis
- **Python**: Backend processing
- **Dummy Data**: Realistic banking scenarios

## Key Features Summary (1 minute)

1. ✅ **Automatic Code Mapping** - Stack traces → Code locations
2. ✅ **AI-Powered Analysis** - GPT-4 explains root causes
3. ✅ **Anomaly Detection** - Catches issues early
4. ✅ **Actionable Insights** - Immediate fixes + prevention strategies
5. ✅ **Banking Focus** - Financial transaction expertise

## Future Enhancements (1 minute)

- Real-time integration with Splunk, AppDynamics
- Git repository integration for live code
- Slack/Teams alerts
- Historical trend analysis
- Automated ticket creation

## Q&A Preparation

### Expected Questions:

**Q: "Is this using real data?"**
A: "For the POC, we're using realistic dummy data simulating a payment processing system. In production, it would integrate with Splunk for logs, Git for code, and AppDynamics for metrics."

**Q: "How accurate is the AI analysis?"**
A: "We're using GPT-4 Turbo with specialized prompts for financial systems. The analysis is highly accurate for common patterns. The more domain context we provide, the better it gets."

**Q: "Can it handle multiple microservices?"**
A: "Yes! The code mapper can load multiple repositories. We'd extend it to map across service boundaries."

**Q: "How long does analysis take?"**
A: "Currently 5-10 seconds. In production, we'd cache common patterns and parallelize analysis for speed."

**Q: "What about security/compliance?"**
A: "Good question! We can use on-premise LLMs or Azure OpenAI with compliance features. All sensitive data can be masked before analysis."

**Q: "Cost of running this?"**
A: "GPT-4 API calls cost ~$0.01-0.05 per analysis. Given it saves hours of engineer time, ROI is massive. We can also use GPT-3.5 for simpler cases."

## Demo Tips

✅ **DO:**

- Speak confidently about the tech
- Emphasize time savings
- Show the code mapping feature - it's the coolest part!
- Explain how this helps the business (fewer failed payments)
- Point out specific line numbers and functions

❌ **DON'T:**

- Get lost in technical details
- Apologize for it being "just a POC"
- Ignore questions
- Rush through the demo

## Backup Plan

If something breaks:

1. Have screenshots ready
2. Explain what it WOULD show
3. Show the code instead
4. Walk through the dummy data

## Time Allocation

- Introduction: 1 min
- Problem: 1 min
- Demo: 8 min
- Architecture: 2 min
- Features: 1 min
- Future: 1 min
- Q&A: 6 min (if 20 min total)

---

**Remember**: You built something impressive in 10 hours. Own it! 🚀
