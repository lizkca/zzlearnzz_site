import time
from functools import wraps
from django.db import connection
from django.conf import settings

def query_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        reset_queries()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        if settings.DEBUG:
            queries = len(connection.queries)
            print(f'Function: {func.__name__}')
            print(f'Number of Queries: {queries}')
            print(f'Finished in: {(end_time - start_time):.2f}s')
        
        return result
    return wrapper
