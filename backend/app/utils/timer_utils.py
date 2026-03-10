"""
  filename      : timer_utils
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
import time

class timer:
    """
    上下文管理器：计时工具
    使用方式：
    with timer() as t:
        do_something()
    print(t.elapsed)  # 输出耗时（秒）
    """
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start