#!/usr/bin/env python3
"""
Test script to verify anomaly detection is working correctly
"""
import json
from src.utils.anomaly_detector import AnomalyDetector
from src.utils.code_mapper import CodeMapper
from src.config import Config

def main():
    print("🧪 Testing Anomaly Detection System\n")
    print("=" * 60)
    
    # Initialize detector
    detector = AnomalyDetector()
    mapper = CodeMapper(Config.CODEBASE_DIR)
    
    # Load sample log
    print("\n1. Loading payment service log...")
    with open(Config.LOGS_DIR + "/payment_service.log", 'r') as f:
        log_content = f.read()
    
    # Test log analysis
    print("\n2. Analyzing logs for anomalies...")
    log_anomalies = detector.analyze_logs(log_content)
    print(f"   ✓ Found {log_anomalies['total_anomalies']} log anomalies")
    print(f"   ✓ Errors: {log_anomalies['error_count']}")
    print(f"   ✓ Critical: {log_anomalies['critical_count']}")
    
    # Show sample anomalies
    print("\n3. Sample log anomalies:")
    for i, anomaly in enumerate(log_anomalies['anomalies'][:3], 1):
        severity = anomaly.get('severity', 'UNKNOWN')
        keyword = anomaly.get('keyword', 'unknown')
        time = anomaly.get('timestamp', 'unknown')
        print(f"   {i}. [{severity}] '{keyword}' at {time}")
    
    # Load and test metrics
    print("\n4. Loading system metrics...")
    with open(Config.METRICS_DIR + "/system_metrics.json", 'r') as f:
        metrics_data = json.load(f)
    
    print("\n5. Analyzing metrics for anomalies...")
    metric_anomalies = detector.analyze_metrics(metrics_data)
    print(f"   ✓ Found {metric_anomalies['total_anomalies']} metric anomalies")
    
    # Show sample metric anomalies
    print("\n6. Sample metric anomalies:")
    for i, anomaly in enumerate(metric_anomalies['anomalies'][:3], 1):
        severity = anomaly.get('severity', 'UNKNOWN')
        message = anomaly.get('message', anomaly.get('type', 'unknown'))
        time = anomaly.get('time', anomaly.get('timestamp', 'unknown'))
        print(f"   {i}. [{severity}] {message} at {time}")
    
    # Test code mapper
    print("\n7. Testing code mapper...")
    code_context = mapper.map_error_to_code(log_content)
    print(f"   ✓ Found {len(code_context.get('stack_trace', []))} stack frames")
    print(f"   ✓ Mapped {len(code_context.get('code_contexts', []))} code contexts")
    
    if code_context.get('code_contexts'):
        ctx = code_context['code_contexts'][0]
        print(f"   ✓ Root cause: {ctx['file']} line {ctx['error_line']} in {ctx.get('function', 'unknown')}")
    
    # Combined summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    total_anomalies = log_anomalies['total_anomalies'] + metric_anomalies['total_anomalies']
    print(f"Total anomalies detected: {total_anomalies}")
    print(f"  - From logs: {log_anomalies['total_anomalies']}")
    print(f"  - From metrics: {metric_anomalies['total_anomalies']}")
    print(f"Code mapping: {len(code_context.get('code_contexts', []))} contexts")
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    main()
