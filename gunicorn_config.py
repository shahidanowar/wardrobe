bind = "0.0.0.0:10000"
workers = 4  # Increased from 2 for better performance
threads = 4  # Increased from 2 for better concurrency
timeout = 120
worker_class = "gthread"
max_requests = 1000
max_requests_jitter = 50
