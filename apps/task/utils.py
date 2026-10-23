import functools
import time
from django.db import connection, reset_queries


def query_debugger(func):
    """
    Декоратор для профилирования и отладки (Debugging & Optimization):
    - Считает количество выполненных SQL-запросов
    - Замеряет точное время выполнения функции (в миллисекундах)
    - Выводит детальную информацию в консоль для анализа проблем (например, N+1)
    """
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        end_queries = len(connection.queries)
        total_time = (end_time - start_time) * 1000
        total_queries = end_queries - start_queries

        print("\n" + "=" * 60)
        print("[DEBUG & OPTIMIZATION REPORT]")
        print(f"-> Method / Function : {func.__name__}")
        print(f"-> SQL Queries Count : {total_queries}")
        print(f"-> Execution Time    : {total_time:.2f} ms")
        if total_queries > 0:
            print("-> Recent SQL queries:")
            for i, q in enumerate(connection.queries[-min(total_queries, 5):], 1):
                sql_snippet = q['sql'].strip().replace('"', '')
                print(f"   {i}. [{q['time']}s] {sql_snippet[:120]}...")
        print("=" * 60 + "\n")

        return result

    return inner_func
