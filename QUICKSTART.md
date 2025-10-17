# Quick Start Guide - GenAI Live Environment Assistant

Welcome to the project! This guide will help you get started quickly. 🚀

## Prerequisites
- Python 3.9+
- Azure OpenAI access with GPT-4 deployment ([Setup Guide](AZURE_SETUP_GUIDE.md))

## Setup (5 minutes)

### 1. Make setup script executable and run it
```bash
chmod +x setup.sh run.sh
./setup.sh
```

### 2. Add your Azure OpenAI credentials
Edit the `.env` file:
```bash
nano .env
# or
code .env
```

Add your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your-api-key-from-azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Don't have these?** See `AZURE_SETUP_GUIDE.md` for detailed instructions!

### 3. Run the application
```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
streamlit run app.py
```

## Project Structure Overview

```
📁 Project Root
├── 📄 app.py                    # Main Streamlit application (START HERE!)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Your API keys (create from .env.example)
│
├── 📁 src/
│   ├── 📄 config.py            # Configuration settings
│   ├── 📁 agents/
│   │   └── 📄 log_analyzer.py  # AI analysis using LangChain + GPT-4
│   └── 📁 utils/
│       ├── 📄 code_mapper.py   # Maps logs to code
│       └── 📄 anomaly_detector.py  # Detects anomalies
│
├── 📁 dummy_data/
│   ├── 📁 logs/                # Simulated error logs
│   ├── 📁 metrics/             # System metrics
│   └── 📁 codebase/            # Sample banking code
```

## How It Works (10-Hour Project Breakdown)

### Phase 1: Understanding (1 hour) ✅ DONE!
- Review the codebase structure
- Understand the dummy data
- Run the application once

### Phase 2: Core Features (4 hours)
**You're here!** The core is built. Now enhance:

1. **Log Analysis** (1 hour)
   - File: `src/agents/log_analyzer.py`
   - Experiment with different prompts
   - Add more error scenarios

2. **Code Mapping** (1 hour)
   - File: `src/utils/code_mapper.py`
   - Enhance error detection
   - Add more code context

3. **UI Enhancement** (2 hours)
   - File: `app.py`
   - Add charts/graphs
   - Improve visualizations

### Phase 3: Banking Scenarios (3 hours)

1. **Add More Scenarios** (1 hour)
   - Create more realistic logs in `dummy_data/logs/`
   - Examples: circuit breaker failures, API timeouts, etc.

2. **Enhance Metrics** (1 hour)
   - File: `dummy_data/metrics/system_metrics.json`
   - Add more banking-specific metrics

3. **AI Improvements** (1 hour)
   - Improve prompts in `log_analyzer.py`
   - Add more banking domain knowledge

### Phase 4: Demo Preparation (2 hours)

1. **Create Demo Script** (1 hour)
   - Prepare 3-4 scenarios to show
   - Practice the flow

2. **Polish & Test** (1 hour)
   - Fix bugs
   - Improve UI/UX
   - Test end-to-end

## Key Files to Customize

### 1. Adding New Error Scenarios
Edit: `dummy_data/logs/payment_service.log`
```log
2024-10-17 10:00:00,000 ERROR [payment_service.py:50] Your error here
```

### 2. Modifying AI Analysis
Edit: `src/agents/log_analyzer.py`
- Change `SYSTEM_PROMPT` for different analysis style
- Modify `_build_analysis_prompt` for more context

### 3. Improving UI
Edit: `app.py`
- Add new Streamlit components
- Change layout and styling
- Add more visualizations

## Testing Your Changes

1. **Quick test**:
   ```bash
   streamlit run app.py
   ```

2. **Test without API calls** (save API costs):
   - Comment out the API call in `log_analyzer.py`
   - Return mock data for testing

## Demo Scenarios Included

1. **SQL Lock Timeout & Deadlock** 🔒
   - Shows database deadlock between transactions
   - Demonstrates lock contention

2. **Connection Pool Exhaustion** 💥
   - Shows what happens when DB connections run out
   - Demonstrates cascading failures

3. **Combined Analysis** 📊
   - Shows multiple issues at once
   - Demonstrates anomaly detection

## Tips for Your 10-Hour Sprint

### Hour 1-2: Get it Running
- ✅ Setup complete
- ✅ Run the app once
- ✅ Understand the flow

### Hour 3-5: Customize
- Add your own error scenarios
- Modify the banking code
- Enhance the AI prompts

### Hour 6-8: Enhance
- Add charts using Plotly
- Improve the UI
- Add more features

### Hour 9-10: Polish & Practice
- Test everything
- Prepare demo script
- Fix bugs

## Common Issues & Solutions

### "Import Error: No module named..."
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "OpenAI API Error"
- Check your API key in `.env`
- Verify you have credits in your OpenAI account

### "File Not Found"
- Make sure you're in the project root directory
- Check paths in `src/config.py`

## Cool Features to Add (If You Have Time)

1. **Real-time Log Streaming** 
   - Use `streamlit.empty()` to simulate live logs

2. **Timeline Visualization**
   - Show error timeline with Plotly

3. **Comparison View**
   - Compare multiple error scenarios side-by-side

4. **Export Reports**
   - Download analysis as PDF

5. **Chat Interface**
   - Ask questions about the errors

## Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Docs](https://platform.openai.com/docs/introduction)

## Need Help?

Check these files for examples:
- `app.py` - Main UI logic
- `src/agents/log_analyzer.py` - AI integration
- `dummy_data/logs/*.log` - Log format examples

---

**Ready to build something awesome! Let's go! 🚀**
