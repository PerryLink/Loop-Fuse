"""loop-fuse: 循环检测和熔断器，防止 AI Agent 陷入死循环"""

from .core import LoopFuse
from .decorators import loop_fuse
from .exceptions import LoopDetectedError

__version__ = "0.1.0"
__all__ = ["LoopFuse", "loop_fuse", "LoopDetectedError"]
