from functools import wraps
from typing import Callable, Optional
from .core import LoopFuse

def loop_fuse(
    window_size: int = 5,
    threshold: int = 3,
    cost_per_call: float = 0.0,
    on_loop_detected: Optional[Callable] = None
):
    """循环检测装饰器"""
    fuse = LoopFuse(window_size, threshold, cost_per_call, on_loop_detected)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                fuse.monitor(args[0])
            return func(*args, **kwargs)
        return wrapper
    return decorator
