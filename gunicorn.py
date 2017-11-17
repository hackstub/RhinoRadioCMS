import multiprocessing

bind = "127.0.0.1:8000"
backlog = 2048

workers = multiprocessing.cpu_count() * 2 + 1

user = 1000

limit_request_line = 2048
limit_request_fields = 50
limit_request_field_size = 4096
