"""
Log Analyzer Agent - Uses LangChain and Azure OpenAI GPT-4 to analyze logs and provide insights
"""
from typing import Dict, Optional
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage


class LogAnalyzerAgent:
    """AI-powered log analysis using GPT-4 and LangChain"""
    
    SYSTEM_PROMPT = """You are an expert DevOps engineer and system reliability expert specializing in analyzing production issues, particularly in financial services and payment systems.

Your role is to:
1. Analyze error logs and stack traces to identify root causes
2. Explain technical issues in clear, actionable terms
3. Provide specific recommendations for fixing issues
4. Identify patterns that led to the failure
5. Suggest preventive measures

Focus on:
- Database issues (deadlocks, lock timeouts, connection pool exhaustion)
- Transaction failures and rollbacks
- Performance bottlenecks
- Concurrency issues
- SQL transaction management

Be specific about:
- Which file, function, and line caused the issue
- The exact error and why it happened
- What was happening in the system at that time
- How to fix it immediately
- How to prevent it in the future"""

    def __init__(self, api_key: str, endpoint: str, deployment_name: str, 
                 api_version: str = "2024-02-15-preview", temperature: float = 0.2):
        """Initialize the analyzer with Azure OpenAI credentials"""
        self.llm = AzureChatOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            azure_deployment=deployment_name,
            temperature=temperature
        )
    
    def analyze_error(self, log_content: str, code_context: Optional[Dict] = None, 
                     metrics: Optional[Dict] = None) -> Dict:
        """
        Analyze an error log with optional code context and metrics
        
        Args:
            log_content: The error log content
            code_context: Code context from CodeMapper
            metrics: System metrics from AnomalyDetector
            
        Returns:
            Dict with AI analysis and recommendations
        """
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(log_content, code_context, metrics)
        
        # Get AI analysis
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            analysis_text = response.content
            
            # Parse the analysis
            parsed_analysis = self._parse_analysis(analysis_text)
            
            return {
                'success': True,
                'analysis': analysis_text,
                'parsed': parsed_analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _build_analysis_prompt(self, log_content: str, code_context: Optional[Dict], 
                               metrics: Optional[Dict]) -> str:
        """Build a comprehensive prompt for analysis"""
        prompt_parts = [
            "# Error Log Analysis Request\n",
            "## Error Logs:\n```",
            log_content,
            "```\n"
        ]
        
        # Add code context if available
        if code_context and code_context.get('code_contexts'):
            prompt_parts.append("\n## Code Context:\n")
            for ctx in code_context['code_contexts']:
                prompt_parts.append(f"\n### File: {ctx['file']}, Function: {ctx.get('function', 'unknown')}\n```python")
                for line in ctx['snippet']:
                    marker = ">>> " if line['is_error'] else "    "
                    prompt_parts.append(f"{marker}Line {line['line_num']}: {line['content']}")
                prompt_parts.append("```\n")
        
        # Add metrics if available
        if metrics:
            prompt_parts.append("\n## System Metrics:\n")
            if 'anomalies' in metrics:
                prompt_parts.append(f"Total Anomalies Detected: {metrics.get('total_anomalies', 0)}\n")
                for anomaly in metrics['anomalies'][:5]:  # Top 5 anomalies
                    prompt_parts.append(f"- [{anomaly.get('severity', 'UNKNOWN')}] {anomaly.get('message', 'Unknown')}\n")
        
        prompt_parts.append("""
## Analysis Required:

Please provide a detailed analysis with the following sections:

1. **Root Cause**: What exactly caused this error?
2. **Impact**: What was the business impact? (e.g., failed payments, service downtime)
3. **Technical Details**: Explain the technical issue in detail
4. **Affected Components**: Which files, functions, or services are affected?
5. **Immediate Fix**: What should be done right now to resolve this?
6. **Prevention**: How can we prevent this from happening again?
7. **Monitoring**: What should we monitor to detect this earlier next time?

Be specific and actionable. Reference exact line numbers, function names, and files.
""")
        
        return "\n".join(prompt_parts)
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parse the AI analysis into structured data"""
        # Simple parsing - extract key sections
        sections = {
            'root_cause': '',
            'impact': '',
            'technical_details': '',
            'affected_components': '',
            'immediate_fix': '',
            'prevention': '',
            'monitoring': ''
        }
        
        # Try to extract sections based on headers
        import re
        
        patterns = {
            'root_cause': r'\*\*Root Cause\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'impact': r'\*\*Impact\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'technical_details': r'\*\*Technical Details\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'affected_components': r'\*\*Affected Components\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'immediate_fix': r'\*\*Immediate Fix\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'prevention': r'\*\*Prevention\*\*:?\s*(.+?)(?=\n\*\*|\Z)',
            'monitoring': r'\*\*Monitoring\*\*:?\s*(.+?)(?=\n\*\*|\Z)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, analysis_text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = match.group(1).strip()
        
        return sections
    
    def generate_incident_summary(self, error_log: str, analysis: Dict) -> str:
        """Generate a concise incident summary"""
        prompt = f"""Based on this error and analysis, create a concise incident summary (2-3 sentences) suitable for an incident report or alert:

ERROR LOG:
{error_log[:500]}...

ANALYSIS:
{analysis.get('analysis', '')[:500]}...

Provide only the summary, no additional text."""

        messages = [
            SystemMessage(content="You are an expert at writing concise incident summaries."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except:
            return "Unable to generate summary"
    
    def suggest_related_issues(self, error_type: str) -> list:
        """Suggest related issues that might occur"""
        prompt = f"""Given this type of error: "{error_type}"

List 3-4 related issues that commonly occur alongside this error in production payment systems.
Format as a simple bulleted list, one issue per line."""

        messages = [
            SystemMessage(content="You are an expert at identifying related production issues."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            issues = [line.strip('- ').strip() for line in response.content.split('\n') if line.strip()]
            return issues[:4]
        except:
            return []
