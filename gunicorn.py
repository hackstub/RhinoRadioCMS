import multiprocessing

bind = "127.0.0.1:5000"
bind = "[::1]:5000"
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048

# Security

limit_request_line = 2048
limit_request_fields = 50
limit_request_field_size = 4096
user = 1000
