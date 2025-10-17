"""
Create additional error scenarios for the demo
Run this script to generate more diverse log examples
"""

# Scenario 4: API Timeout
api_timeout_log = """2024-10-17 10:30:15,234 INFO [payment_service.py:16] PaymentService initialized
2024-10-17 10:30:45,567 INFO [payment_service.py:27] Processing payment PMT20241017103045: $5000.00 from ACC10678 to ACC20901
2024-10-17 10:30:45,789 DEBUG [external_api.py:45] Calling fraud detection API for payment PMT20241017103045
2024-10-17 10:30:45,790 DEBUG [external_api.py:52] POST https://api.fraudcheck.bank.com/v1/verify
2024-10-17 10:31:15,791 ERROR [external_api.py:58] Request timeout after 30.0s
2024-10-17 10:31:15,792 ERROR [external_api.py:60] HTTPConnectionPool(host='api.fraudcheck.bank.com', port=443): Read timed out. (read timeout=30)
Traceback (most recent call last):
  File "/app/dummy_data/codebase/external_api.py", line 56, in call_fraud_api
    response = requests.post(url, json=payload, timeout=30)
  File "/usr/lib/python3.9/site-packages/requests/api.py", line 119, in post
    return request('post', url, data=data, json=json, **kwargs)
  File "/usr/lib/python3.9/site-packages/requests/adapters.py", line 486, in send
    raise ReadTimeout(e, request=request)
requests.exceptions.ReadTimeout: HTTPConnectionPool(host='api.fraudcheck.bank.com', port=443): Read timed out.
2024-10-17 10:31:15,800 WARNING [payment_service.py:35] Fraud check failed for payment PMT20241017103045
2024-10-17 10:31:15,801 ERROR [payment_service.py:44] Error processing payment PMT20241017103045: Fraud check service unavailable
"""

# Scenario 5: Memory Leak
memory_leak_log = """2024-10-17 11:15:00,123 INFO [payment_processor.py:89] Batch processing started: 5000 payments
2024-10-17 11:15:30,456 DEBUG [payment_processor.py:102] Processed 1000 payments, memory usage: 1.2GB
2024-10-17 11:16:00,789 DEBUG [payment_processor.py:102] Processed 2000 payments, memory usage: 2.8GB
2024-10-17 11:16:30,012 DEBUG [payment_processor.py:102] Processed 3000 payments, memory usage: 4.5GB
2024-10-17 11:17:00,345 WARNING [payment_processor.py:102] Processed 4000 payments, memory usage: 6.2GB
2024-10-17 11:17:15,678 CRITICAL [payment_processor.py:108] High memory usage detected: 7.8GB/8GB (97%)
2024-10-17 11:17:20,901 ERROR [payment_processor.py:115] MemoryError: Unable to allocate memory
Traceback (most recent call last):
  File "/app/dummy_data/codebase/payment_processor.py", line 112, in process_batch
    results.append(self.process_payment(payment))
  File "/app/dummy_data/codebase/payment_processor.py", line 134, in process_payment
    transaction_log = self.create_transaction_log(payment_id, details)
MemoryError: Unable to allocate 512.0 MiB for array with shape (134217728,) and data type object
2024-10-17 11:17:20,905 ERROR [payment_processor.py:120] Batch processing failed after 4234 payments
"""

# Scenario 6: Cascading Failure
cascading_failure_log = """2024-10-17 12:00:00,000 INFO [load_balancer.py:45] Health check: All 3 payment service instances healthy
2024-10-17 12:00:30,123 ERROR [payment_service_1.py:78] Database connection failed: Connection refused
2024-10-17 12:00:30,124 WARNING [load_balancer.py:52] Instance payment_service_1 unhealthy, removing from pool
2024-10-17 12:00:45,456 INFO [load_balancer.py:58] Routing traffic to 2 remaining instances
2024-10-17 12:01:15,789 ERROR [payment_service_2.py:78] Database connection failed: Connection refused
2024-10-17 12:01:15,790 WARNING [load_balancer.py:52] Instance payment_service_2 unhealthy, removing from pool
2024-10-17 12:01:30,012 CRITICAL [load_balancer.py:65] Only 1 instance remaining, load at 300%
2024-10-17 12:02:00,345 ERROR [payment_service_3.py:91] CPU at 99%, request queue at 450
2024-10-17 12:02:05,678 ERROR [payment_service_3.py:78] Database connection failed: Too many connections
2024-10-17 12:02:05,679 CRITICAL [load_balancer.py:70] All payment service instances down
2024-10-17 12:02:05,680 CRITICAL [load_balancer.py:72] SERVICE OUTAGE: Payment processing unavailable
"""

print("📝 Additional error scenarios created!")
print("\nThese scenarios demonstrate:")
print("1. API Timeout - External service failures")
print("2. Memory Leak - Resource exhaustion")  
print("3. Cascading Failure - System-wide outage")
print("\nYou can add these to your dummy_data/logs/ directory for more demos!")
