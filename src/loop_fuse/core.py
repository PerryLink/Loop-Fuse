from collections import deque
from typing import Any, Callable, Optional
from .fingerprint import generate_fingerprint
from .exceptions import LoopDetectedError
from .ui import display_circuit_break_warning
from .logger import save_loop_log

class LoopFuse:
    def __init__(
        self,
        window_size: int = 5,
        threshold: int = 3,
        cost_per_call: float = 0.0,
        on_loop_detected: Optional[Callable] = None
    ):
        self.history = deque(maxlen=window_size)
        self.threshold = threshold
        self.cost_per_call = cost_per_call
        self.on_loop_detected = on_loop_detected
        self.call_count = 0

    def monitor(self, action: Any) -> None:
        """监控单次操作"""
        fingerprint = generate_fingerprint(action)
        self.history.append((fingerprint, action))
        self.call_count += 1

        count = sum(1 for fp, _ in self.history if fp == fingerprint)

        if count >= self.threshold:
            self._trigger_circuit_break(fingerprint, action)

    def _trigger_circuit_break(self, fingerprint: str, action: Any) -> None:
        """触发熔断机制"""
        cost_saved = self.cost_per_call * (self.call_count - len(self.history))

        if self.on_loop_detected:
            self.on_loop_detected(list(self.history), fingerprint, cost_saved)

        save_loop_log(list(self.history), fingerprint, cost_saved)
        display_circuit_break_warning(list(self.history), fingerprint, cost_saved)

        raise LoopDetectedError(
            f"循环检测到！指纹 {fingerprint[:8]} 重复 {self.threshold} 次"
        )
