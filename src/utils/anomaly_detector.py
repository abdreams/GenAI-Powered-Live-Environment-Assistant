"""
Anomaly Detector - Detects unusual patterns in logs and metrics
"""
import re
from typing import Dict, List
from datetime import datetime


class AnomalyDetector:
    """Detects anomalies in logs and system metrics"""
    
    # Error keywords and their severity
    ERROR_KEYWORDS = {
        'CRITICAL': ['deadlock', 'pool exhausted', 'timeout exceeded', 'connection failed'],
        'HIGH': ['lock timeout', 'transaction failed', 'rollback', 'wait timeout'],
        'MEDIUM': ['lock contention', 'waiting for lock', 'connection queued'],
        'LOW': ['warning', 'retry', 'slow query']
    }
    
    # Thresholds for metric anomalies
    THRESHOLDS = {
        'connection_pool_usage': 0.8,  # 80%
        'error_rate': 0.15,  # 15%
        'avg_response_time_ms': 500,
        'queue_size': 3
    }
    
    def analyze_logs(self, log_content: str) -> Dict:
        """
        Analyze log content for anomalies
        
        Returns:
            Dict with detected anomalies and statistics
        """
        lines = log_content.split('\n')
        
        anomalies = []
        error_count = 0
        warning_count = 0
        critical_count = 0
        
        for line in lines:
            # Check error levels
            if 'ERROR' in line or 'CRITICAL' in line:
                error_count += 1
                
                # Check for specific critical patterns
                for severity, keywords in self.ERROR_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword.lower() in line.lower():
                            anomalies.append({
                                'type': 'log_pattern',
                                'severity': severity,
                                'keyword': keyword,
                                'line': line.strip(),
                                'timestamp': self._extract_timestamp(line)
                            })
                            
                            if severity == 'CRITICAL':
                                critical_count += 1
            
            if 'WARNING' in line:
                warning_count += 1
        
        return {
            'total_anomalies': len(anomalies),
            'error_count': error_count,
            'warning_count': warning_count,
            'critical_count': critical_count,
            'anomalies': anomalies
        }
    
    def analyze_metrics(self, metrics_data: Dict) -> Dict:
        """
        Analyze system metrics for anomalies
        
        Returns:
            Dict with metric anomalies
        """
        anomalies = []
        
        if 'metrics' in metrics_data:
            for metric in metrics_data['metrics']:
                time = metric.get('time', 'unknown')
                
                # Check connection pool usage
                active_conns = metric.get('active_connections', 0)
                max_conns = 10  # From our DatabaseManager
                pool_usage = active_conns / max_conns
                
                if pool_usage >= self.THRESHOLDS['connection_pool_usage']:
                    anomalies.append({
                        'type': 'connection_pool_high',
                        'severity': 'HIGH' if pool_usage >= 0.9 else 'MEDIUM',
                        'time': time,
                        'value': f"{active_conns}/{max_conns} ({pool_usage*100:.0f}%)",
                        'message': f"Connection pool usage at {pool_usage*100:.0f}%"
                    })
                
                # Check error rate
                error_rate = metric.get('error_rate', 0)
                if error_rate >= self.THRESHOLDS['error_rate']:
                    anomalies.append({
                        'type': 'error_rate_high',
                        'severity': 'HIGH' if error_rate >= 0.25 else 'MEDIUM',
                        'time': time,
                        'value': f"{error_rate*100:.1f}%",
                        'message': f"Error rate at {error_rate*100:.1f}%"
                    })
                
                # Check response time
                response_time = metric.get('avg_response_time_ms', 0)
                if response_time >= self.THRESHOLDS['avg_response_time_ms']:
                    anomalies.append({
                        'type': 'response_time_high',
                        'severity': 'HIGH' if response_time >= 1000 else 'MEDIUM',
                        'time': time,
                        'value': f"{response_time}ms",
                        'message': f"Average response time at {response_time}ms"
                    })
                
                # Check queue size
                queue_size = metric.get('queue_size', 0)
                if queue_size >= self.THRESHOLDS['queue_size']:
                    anomalies.append({
                        'type': 'queue_size_high',
                        'severity': 'HIGH' if queue_size >= 5 else 'MEDIUM',
                        'time': time,
                        'value': queue_size,
                        'message': f"Connection queue size at {queue_size}"
                    })
        
        # Add predefined anomalies from the metrics data
        if 'anomalies' in metrics_data:
            for anomaly in metrics_data['anomalies']:
                anomalies.append({
                    'type': anomaly.get('type', 'unknown'),
                    'severity': anomaly.get('severity', 'MEDIUM').upper(),
                    'time': anomaly.get('timestamp', 'unknown'),
                    'message': anomaly.get('description', 'Unknown anomaly')
                })
        
        return {
            'total_anomalies': len(anomalies),
            'anomalies': sorted(anomalies, key=lambda x: self._severity_to_int(x['severity']), reverse=True)
        }
    
    def _extract_timestamp(self, log_line: str) -> str:
        """Extract timestamp from log line"""
        # Pattern: 2024-10-17 09:15:45,145
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'
        match = re.search(pattern, log_line)
        return match.group(0) if match else 'unknown'
    
    def _severity_to_int(self, severity: str) -> int:
        """Convert severity to int for sorting"""
        severity_map = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        return severity_map.get(severity.upper(), 0)
    
    def get_severity_color(self, severity: str) -> str:
        """Get color code for severity level"""
        colors = {
            'CRITICAL': '#FF0000',
            'HIGH': '#FF6B6B',
            'MEDIUM': '#FFA500',
            'LOW': '#FFD700'
        }
        return colors.get(severity.upper(), '#808080')
