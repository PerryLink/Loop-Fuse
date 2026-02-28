import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Any

def save_loop_log(
    history: List[Tuple[str, Any]],
    fingerprint: str,
    cost_saved: float
) -> None:
    """保存熔断日志到文件"""
    log_dir = Path(".loop-fuse-logs")
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"loop_{timestamp}.json"

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "fingerprint": fingerprint,
        "cost_saved": cost_saved,
        "history": [
            {"fingerprint": fp, "action": str(action)}
            for fp, action in history
        ]
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
