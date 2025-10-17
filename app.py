"""
GenAI-Powered Live Environment Assistant
Main Streamlit Application
"""
import streamlit as st
import json
import os
from pathlib import Path

# Import our custom modules
from src.config import Config
from src.agents.log_analyzer import LogAnalyzerAgent
from src.utils.code_mapper import CodeMapper
from src.utils.anomaly_detector import AnomalyDetector

# Page configuration
st.set_page_config(
    page_title="GenAI Live Environment Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #000000;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #000000;
    }
    .code-highlight {
        background-color: #fff3cd;
        border-left: 3px solid #ff9800;
        padding: 0.5rem;
        margin: 0.2rem 0;
        color: #000000;
        font-family: monospace;
    }
    .anomaly-critical {
        color: #d32f2f;
        font-weight: bold;
    }
    .anomaly-high {
        color: #f57c00;
        font-weight: bold;
    }
    .anomaly-medium {
        color: #ffa726;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'code_context' not in st.session_state:
        st.session_state.code_context = None
    if 'anomalies' not in st.session_state:
        st.session_state.anomalies = None
    if 'log_content' not in st.session_state:
        st.session_state.log_content = None
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""


def load_log_file(log_path: str) -> str:
    """Load log file content"""
    try:
        with open(log_path, 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading log file: {e}")
        return ""


def load_metrics_file(metrics_path: str) -> dict:
    """Load metrics JSON file"""
    try:
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading metrics file: {e}")
        return {}


def display_error_log(log_content: str):
    """Display error log with highlighting"""
    st.markdown("### 📋 Error Logs")
    
    # Extract error section (last 20 lines for brevity)
    lines = log_content.split('\n')
    error_lines = []
    
    for i, line in enumerate(lines):
        if 'ERROR' in line or 'CRITICAL' in line or 'Traceback' in line:
            # Show context around errors
            start = max(0, i - 2)
            end = min(len(lines), i + 10)
            error_lines.extend(lines[start:end])
            break
    
    if not error_lines:
        error_lines = lines[-20:]
    
    st.code('\n'.join(error_lines), language='log')


def display_code_context(code_context: dict):
    """Display code context with error highlighting"""
    st.markdown("### 💻 Code Context")
    
    if not code_context or not code_context.get('code_contexts'):
        st.info("ℹ️ No specific code context mapped. The error may not contain a stack trace, or the files may not be in the codebase directory.")
        return
    
    for ctx in code_context['code_contexts']:
        file_name = ctx.get('file', 'unknown')
        function_name = ctx.get('function', 'unknown')
        error_line = ctx.get('error_line', 'unknown')
        
        with st.expander(f"📄 {file_name} - Function: `{function_name}`", expanded=False):
            st.markdown(f"**Error at line {error_line}**")
            
            # Display code with highlighting
            snippet = ctx.get('snippet', [])
            if snippet:
                for line in snippet:
                    line_num = line.get('line_num', '?')
                    content = line.get('content', '')
                    is_error = line.get('is_error', False)
                    
                    if is_error:
                        st.markdown(f"<div class='code-highlight'>❌ Line {line_num}: {content}</div>", 
                                  unsafe_allow_html=True)
                    else:
                        st.code(f"Line {line_num}: {content}", language='python')
            else:
                st.warning("No code snippet available")


def display_ai_analysis(analysis: dict):
    """Display AI-powered analysis"""
    st.markdown("### 🤖 AI Analysis")
    
    if not analysis or not analysis.get('success'):
        st.error(f"Analysis failed: {analysis.get('error', 'Unknown error')}")
        return
    
    parsed = analysis.get('parsed', {})
    
    # Root Cause
    if parsed.get('root_cause'):
        st.markdown("#### 🎯 Root Cause")
        st.markdown(f"<div class='error-box'>{parsed['root_cause']}</div>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["💥 Impact", "🔧 Technical Details", "⚡ Immediate Fix", "🛡️ Prevention", "📊 Monitoring"])
    
    with tabs[0]:
        st.markdown(parsed.get('impact', 'No impact analysis available'))
    
    with tabs[1]:
        st.markdown(parsed.get('technical_details', 'No technical details available'))
    
    with tabs[2]:
        st.markdown(f"<div class='success-box'>{parsed.get('immediate_fix', 'No fix recommendations available')}</div>", 
                   unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown(parsed.get('prevention', 'No prevention recommendations available'))
    
    with tabs[4]:
        st.markdown(parsed.get('monitoring', 'No monitoring recommendations available'))
    
    # Full analysis in expander
    with st.expander("📝 Full Analysis"):
        st.markdown(analysis.get('analysis', ''))


def display_anomalies(anomalies: dict):
    """Display detected anomalies"""
    st.markdown("### ⚠️ Detected Anomalies")
    
    total = anomalies.get('total_anomalies', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Anomalies", total)
    with col2:
        critical = sum(1 for a in anomalies.get('anomalies', []) if a.get('severity') == 'CRITICAL')
        st.metric("Critical", critical)
    with col3:
        high = sum(1 for a in anomalies.get('anomalies', []) if a.get('severity') == 'HIGH')
        st.metric("High", high)
    
    st.markdown("---")
    
    # List anomalies
    for anomaly in anomalies.get('anomalies', [])[:10]:
        severity = anomaly.get('severity', 'UNKNOWN')
        
        # Build message from available fields
        if 'message' in anomaly:
            message = anomaly['message']
        elif 'keyword' in anomaly:
            message = f"Detected '{anomaly['keyword']}' pattern in logs"
        elif 'line' in anomaly:
            message = anomaly['line'][:100]  # Truncate long lines
        else:
            message = f"{anomaly.get('type', 'Unknown')} anomaly"
        
        # Get timestamp
        time = anomaly.get('time') or anomaly.get('timestamp', 'unknown')
        
        severity_class = f"anomaly-{severity.lower()}"
        st.markdown(f"<span class='{severity_class}'>🔴 [{severity}]</span> {message} (at {time})", 
                   unsafe_allow_html=True)


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown("<h1 class='main-header'>🤖 GenAI Live Environment Assistant</h1>", unsafe_allow_html=True)
    st.markdown("**AI-Powered Production Monitoring & Root Cause Analysis**")
    
    # Top metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🟢 System Health", "92%", "+2%")
    with col2:
        st.metric("⚠️ Active Alerts", "7", "-3")
    with col3:
        st.metric("📊 Avg Response Time", "245ms", "-15ms")
    with col4:
        st.metric("🔄 Uptime", "99.8%", "+0.1%")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Azure OpenAI Configuration (collapsible)
        with st.expander("🔐 Azure OpenAI Settings", expanded=False):
            api_key = st.text_input("API Key", type="password", 
                                   help="Enter your Azure OpenAI API key")
            
            endpoint = st.text_input("Endpoint", 
                                    help="e.g., https://your-resource.openai.azure.com/")
            
            deployment_name = st.text_input("Deployment",
                                           help="e.g., gpt-4")
            
            # Load from environment if not provided
            if not api_key:
                api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
            if not endpoint:
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
            if not deployment_name:
                deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
        
        st.markdown("---")
        
        st.header(" Data Source Integrations")
        
        # Integration status
        integrations = {
            "AppDynamics": {"icon": "📊", "status": "🟢 Connected", "color": "green"},
            "Splunk": {"icon": "🔍", "status": "🟢 Connected", "color": "green"},
            "SQL Server": {"icon": "🗄️", "status": "🟢 Connected", "color": "green"},
            "GitHub": {"icon": "💻", "status": "🟢 Connected", "color": "green"},
            "Prometheus": {"icon": "📈", "status": "🟡 Standby", "color": "orange"},
            "Datadog": {"icon": "🐕", "status": "🟡 Standby", "color": "orange"},
        }
        
        for name, info in integrations.items():
            st.markdown(f"{info['icon']} **{name}**: {info['status']}")
        
        st.markdown("---")
        
        if st.button("⚙️ Configure Integrations", use_container_width=True):
            st.info("Integration settings would open here")
        
        st.markdown("---")
        
        st.header("📅 Time Range")
        time_range = st.selectbox(
            "Select Range",
            ["Last 15 minutes", "Last 1 hour", "Last 4 hours", "Last 24 hours", "Last 7 days"]
        )
        
        st.markdown("---")
        
        st.header("🎯 Environment")
        environment = st.selectbox(
            "Select Environment",
            ["🔴 Production", "🟡 Staging", "🟢 Development"]
        )
    
    # Main content area - Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Ask AI Assistant", "📊 Live Dashboard", "🔍 Deep Dive Analysis"])
    
    with tab1:
        st.markdown("### 💬 AI Assistant - Ask About Production Issues")
        st.markdown("Ask questions about errors, anomalies, performance issues, or get recommendations...")
        
        # Chat-like interface
        user_query = st.text_area(
            "What would you like to know?",
            placeholder="E.g., 'What's causing the high error rate in payment service?'\n'Analyze the recent database connection issues'\n'Show me the root cause of transaction failures'",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.analysis_done = False
                st.rerun()
        
        if not user_query and analyze_button:
            st.warning("⚠️ Please enter a question or describe the issue you're investigating")
        
        if user_query and analyze_button:
            if not api_key or not endpoint or not deployment_name:
                st.error("❌ Please configure Azure OpenAI settings in the sidebar first!")
            else:
                with st.spinner("🔄 AI is analyzing logs, metrics, and code..."):
                    try:
                        # Initialize components
                        code_mapper = CodeMapper(Config.CODEBASE_DIR)
                        anomaly_detector = AnomalyDetector()
                        log_analyzer = LogAnalyzerAgent(
                            api_key=api_key,
                            endpoint=endpoint,
                            deployment_name=deployment_name,
                            api_version=Config.AZURE_OPENAI_API_VERSION
                        )
                        
                        # Load logs
                        payment_log = load_log_file(os.path.join(Config.LOGS_DIR, "payment_service.log"))
                        db_log = load_log_file(os.path.join(Config.LOGS_DIR, "database.log"))
                        
                        # Combine logs for analysis
                        combined_log = f"=== Payment Service Log ===\n{payment_log}\n\n=== Database Log ===\n{db_log}"
                        
                        # Map error to code
                        code_context = code_mapper.map_error_to_code(payment_log)
                        
                        # Detect anomalies
                        log_anomalies = anomaly_detector.analyze_logs(combined_log)
                        metrics_data = load_metrics_file(os.path.join(Config.METRICS_DIR, "system_metrics.json"))
                        metric_anomalies = anomaly_detector.analyze_metrics(metrics_data)
                        
                        # Combine anomalies
                        all_anomalies = {
                            'total_anomalies': log_anomalies['total_anomalies'] + metric_anomalies['total_anomalies'],
                            'anomalies': log_anomalies['anomalies'] + metric_anomalies['anomalies']
                        }
                        
                        # Add user query to the analysis context
                        analysis_context = f"User Question: {user_query}\n\n{combined_log}"
                        
                        # AI Analysis
                        analysis = log_analyzer.analyze_error(
                            log_content=analysis_context,
                            code_context=code_context,
                            metrics=all_anomalies
                        )
                        
                        # Store in session state
                        st.session_state.analysis_done = True
                        st.session_state.current_analysis = analysis
                        st.session_state.code_context = code_context
                        st.session_state.anomalies = all_anomalies
                        st.session_state.log_content = payment_log
                        st.session_state.user_query = user_query
                        
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {e}")
                        import traceback
                        st.code(traceback.format_exc())
        
        # Display results
        if st.session_state.analysis_done and st.session_state.anomalies:
            st.markdown("---")
            st.markdown(f"### 🎯 Analysis Results for: *\"{st.session_state.get('user_query', 'Production Issues')}\"*")
            
            # Create two columns
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.session_state.log_content:
                    display_error_log(st.session_state.log_content)
                st.markdown("---")
                if st.session_state.anomalies:
                    display_anomalies(st.session_state.anomalies)
            
            with col2:
                if st.session_state.code_context:
                    display_code_context(st.session_state.code_context)
            
            st.markdown("---")
            display_ai_analysis(st.session_state.current_analysis)
            
            # Additional info
            with st.expander("📚 View Full Code Files"):
                code_mapper = CodeMapper(Config.CODEBASE_DIR)
                files = code_mapper.get_all_files()
                
                selected_file = st.selectbox("Select a file to view", files)
                if selected_file:
                    content = code_mapper.get_file_content(selected_file)
                    st.code(content, language='python')
    
    with tab2:
        st.markdown("### 📊 Real-Time Monitoring Dashboard")
        
        # Anomalies Overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🚨 Recent Anomalies (Live)")
            
            # Load and display anomalies automatically
            try:
                payment_log = load_log_file(os.path.join(Config.LOGS_DIR, "payment_service.log"))
                db_log = load_log_file(os.path.join(Config.LOGS_DIR, "database.log"))
                combined_log = f"{payment_log}\n{db_log}"
                
                anomaly_detector = AnomalyDetector()
                log_anomalies = anomaly_detector.analyze_logs(combined_log)
                metrics_data = load_metrics_file(os.path.join(Config.METRICS_DIR, "system_metrics.json"))
                metric_anomalies = anomaly_detector.analyze_metrics(metrics_data)
                
                all_anomalies = {
                    'total_anomalies': log_anomalies['total_anomalies'] + metric_anomalies['total_anomalies'],
                    'anomalies': log_anomalies['anomalies'] + metric_anomalies['anomalies']
                }
                
                # Display top 15 anomalies
                for i, anomaly in enumerate(all_anomalies.get('anomalies', [])[:15], 1):
                    severity = anomaly.get('severity', 'UNKNOWN')
                    
                    if 'message' in anomaly:
                        message = anomaly['message']
                    elif 'keyword' in anomaly:
                        message = f"Detected '{anomaly['keyword']}' pattern"
                    else:
                        message = f"{anomaly.get('type', 'Unknown')} anomaly"
                    
                    time = anomaly.get('time') or anomaly.get('timestamp', 'unknown')
                    
                    severity_emoji = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡"
                    st.markdown(f"{severity_emoji} **[{severity}]** {message} • *{time}*")
                
            except Exception as e:
                st.error(f"Error loading dashboard data: {e}")
        
        with col2:
            st.markdown("#### 📈 System Stats")
            st.metric("Error Rate", "12.5%", "↑ 3.2%", delta_color="inverse")
            st.metric("Active Connections", "8/10", "↑ 2")
            st.metric("Queue Size", "5", "↑ 3", delta_color="inverse")
            st.metric("Avg Lock Time", "8.2s", "↑ 2.1s", delta_color="inverse")
            
            st.markdown("---")
            st.markdown("#### 🎯 Top Issues")
            st.markdown("1. 🔴 Connection Pool")
            st.markdown("2. 🔴 Lock Timeouts")
            st.markdown("3. 🟠 Slow Queries")
            st.markdown("4. 🟡 High Memory")
        
        st.markdown("---")
        
        # Service Health
        st.markdown("#### 🏥 Service Health Status")
        
        services = [
            {"name": "Payment Service", "status": "🟡 Degraded", "uptime": "98.2%", "errors": "12"},
            {"name": "Database Service", "status": "🔴 Critical", "uptime": "99.1%", "errors": "8"},
            {"name": "Auth Service", "status": "🟢 Healthy", "uptime": "99.9%", "errors": "0"},
            {"name": "Notification Service", "status": "🟢 Healthy", "uptime": "99.8%", "errors": "1"},
        ]
        
        cols = st.columns(4)
        for i, service in enumerate(services):
            with cols[i]:
                st.markdown(f"**{service['name']}**")
                st.markdown(f"{service['status']}")
                st.markdown(f"Uptime: {service['uptime']}")
                st.markdown(f"Errors: {service['errors']}")
    
    with tab3:
        st.markdown("### 🔍 Deep Dive Analysis")
        st.info("💡 Use the **AI Assistant** tab to analyze specific issues, or select a service below for detailed analysis")
        
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Transaction Flow Analysis", "Database Performance", "Error Pattern Recognition", "Capacity Planning"]
        )
        
        if st.button("📊 Run Deep Analysis", type="primary"):
            st.info("This would trigger a comprehensive deep-dive analysis with the selected focus area")


if __name__ == "__main__":
    main()
