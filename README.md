# GenAI-Powered Live Environment Assistant 🤖

An intelligent assistant that helps DevOps and engineering teams quickly identify and diagnose issues in production environments by mapping error logs and stack traces to actual code.

## 🎯 Features

- **Smart Log Analysis**: AI-powered analysis of error logs and stack traces
- **Code Mapping**: Automatically maps errors to specific files, functions, and lines of code
- **Anomaly Detection**: Identifies unusual patterns in logs and metrics
- **Root Cause Analysis**: Provides intelligent insights on what went wrong
- **Banking Use Case**: Simulates a payment processing system with SQL transaction failures

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   LangChain     │◄────►│   GPT-4      │
│   Agent         │      │   Turbo      │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Dummy Data (Logs + Code + Metrics) │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Azure OpenAI access with GPT-4 deployment

### Installation

1. **Clone the repository**

```bash
cd GenAI-Powered-Live-Environment-Assistant
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up Azure OpenAI credentials**

```bash
cp .env.example .env
# Edit .env and add your Azure OpenAI credentials
# See AZURE_SETUP_GUIDE.md for detailed instructions
```

5. **Run the application**

```bash
streamlit run app.py
```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
GenAI-Powered-Live-Environment-Assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
│
├── src/
│   ├── agents/
│   │   └── log_analyzer.py        # LangChain agent for log analysis
│   ├── utils/
│   │   ├── code_mapper.py         # Maps logs to code
│   │   └── anomaly_detector.py    # Detects anomalies
│   └── config.py                  # Configuration management
│
├── dummy_data/
│   ├── logs/
│   │   ├── payment_service.log    # Simulated payment service logs
│   │   └── database.log           # Simulated database logs
│   ├── metrics/
│   │   └── system_metrics.json    # System performance metrics
│   └── codebase/
│       ├── payment_service.py     # Sample payment processing code
│       ├── database_manager.py    # Sample DB management code
│       └── transaction_handler.py # Sample transaction handling code
│
└── assets/
    └── styles.css                 # Custom CSS for Streamlit
```

## 🎮 Usage

1. **Select a Log File**: Choose from pre-populated error scenarios
2. **View Analysis**: See AI-powered analysis of the error
3. **Explore Code Mapping**: Jump to the exact code causing the issue
4. **Check Recommendations**: Get actionable insights to fix the problem

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Azure OpenAI GPT-4 Turbo, LangChain
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Altair
- **Language**: Python 3.9+

## 📊 Demo Scenarios

### Scenario 1: SQL Transaction Deadlock

Payment processing fails due to database deadlock between concurrent transactions.

### Scenario 2: Connection Pool Exhaustion

High load causes database connection pool to be exhausted, leading to timeouts.

### Scenario 3: Lock Timeout

Long-running transaction holds locks causing other transactions to timeout.

## 🔮 Future Enhancements

- [ ] Real-time log streaming integration (Splunk, ELK)
- [ ] Git integration for actual codebase analysis
- [ ] AppDynamics APM integration
- [ ] Multi-repository support
- [ ] Slack/Teams notifications
- [ ] Historical trend analysis
- [ ] Automated ticket creation (JIRA)
- [ ] Support for both Azure OpenAI and OpenAI API

## 👥 Team

Built with ❤️ for efficient incident response

## 📝 License

MIT License - feel free to use for your projects!
