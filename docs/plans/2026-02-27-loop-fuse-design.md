# loop-fuse 完整设计文档

**日期**: 2026-02-27
**版本**: 1.0
**状态**: 已批准

## 设计决策总结

- **使用方式**: 装饰器模式（`@loop_fuse`）
- **配置方式**: 装饰器参数配置
- **指纹生成**: 字符串哈希（MD5）
- **熔断行为**: 抛出 `LoopDetectedError` 异常
- **日志方式**: 仅在熔断时输出
- **可视化风格**: 简洁文本（使用 rich 库）
- **额外功能**: 保存日志到文件 + 自定义回调 + 成本估算

---

## 1. 整体架构

### 项目结构
```
loop-fuse/
├── src/
│   └── loop_fuse/
│       ├── __init__.py          # 暴露主要 API
│       ├── core.py              # 核心 LoopFuse 类
│       ├── decorators.py        # @loop_fuse 装饰器
│       ├── fingerprint.py       # 指纹生成逻辑
│       ├── exceptions.py        # LoopDetectedError 异常
│       ├── logger.py            # 日志保存逻辑
│       └── ui.py                # Rich 库可视化输出
├── examples/
│   ├── basic_usage.py           # 基础使用示例
│   ├── with_callback.py         # 自定义回调示例
│   └── cost_estimation.py       # 成本估算示例
├── tests/
│   ├── test_core.py             # 核心逻辑测试
│   ├── test_decorators.py       # 装饰器测试
│   └── test_fingerprint.py      # 指纹生成测试
├── docs/
│   └── plans/                   # 设计文档目录
├── .loop-fuse-logs/             # 熔断日志保存目录（运行时生成）
├── README.md
├── pyproject.toml
└── LICENSE
```

### 核心依赖
- `rich`: 终端可视化输出
- `hashlib`: 内置库，用于 MD5 哈希

### 主要 API
```python
# 基础使用
@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    pass

# 带成本估算
@loop_fuse(threshold=3, cost_per_call=0.01)
def agent_loop(action):
    pass

# 自定义回调
@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    pass
```

---

## 2. 核心组件设计

### core.py - LoopFuse 核心类

```python
from collections import deque

class LoopFuse:
    def __init__(
        self,
        window_size: int = 5,
        threshold: int = 3,
        cost_per_call: float = 0.0,
        on_loop_detected: Callable = None
    ):
        self.history = deque(maxlen=window_size)
        self.threshold = threshold
        self.cost_per_call = cost_per_call
        self.on_loop_detected = on_loop_detected
        self.call_count = 0

    def monitor(self, action: Any) -> None:
        fingerprint = generate_fingerprint(action)
        self.history.append((fingerprint, action))
        self.call_count += 1

        count = sum(1 for fp, _ in self.history if fp == fingerprint)

        if count >= self.threshold:
            self._trigger_circuit_break(fingerprint, action)

    def _trigger_circuit_break(self, fingerprint, action):
        cost_saved = self.cost_per_call * (self.call_count - len(self.history))

        if self.on_loop_detected:
            self.on_loop_detected(list(self.history), fingerprint, cost_saved)

        save_loop_log(self.history, fingerprint, cost_saved)
        display_circuit_break_warning(self.history, fingerprint, cost_saved)

        raise LoopDetectedError(f"循环检测到！指纹 {fingerprint[:8]} 重复 {self.threshold} 次")
```

**核心算法**：
- 使用 `deque` 实现固定大小的滚动窗口
- 每次调用 `monitor()` 时计算指纹并检查重复次数
- 达到阈值立即触发熔断

### fingerprint.py - 指纹生成

```python
import hashlib

def generate_fingerprint(action: Any) -> str:
    action_str = str(action)
    return hashlib.md5(action_str.encode('utf-8')).hexdigest()
```

### decorators.py - 装饰器

```python
from functools import wraps

def loop_fuse(
    window_size: int = 5,
    threshold: int = 3,
    cost_per_call: float = 0.0,
    on_loop_detected: Callable = None
):
    fuse = LoopFuse(window_size, threshold, cost_per_call, on_loop_detected)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                fuse.monitor(args[0])
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 3. 可视化与日志设计

### ui.py - 可视化输出

使用 `rich` 库实现简洁的红色警告输出：

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def display_circuit_break_warning(history, fingerprint, cost_saved):
    console = Console()

    warning_text = f"""
[bold red]⚠️  循环检测！系统已熔断 ⚠️[/bold red]

指纹: {fingerprint[:16]}...
重复次数: {sum(1 for fp, _ in history if fp == fingerprint)}
总调用次数: {len(history)}
节省成本: ${cost_saved:.4f}
    """

    console.print(Panel(warning_text, border_style="red", title="LOOP FUSE"))

    table = Table(title="循环历史", show_header=True)
    table.add_column("#", style="dim")
    table.add_column("指纹", style="cyan")
    table.add_column("操作", style="yellow")

    for i, (fp, action) in enumerate(history, 1):
        marker = "🔴" if fp == fingerprint else "⚪"
        table.add_row(
            f"{marker} {i}",
            fp[:8] + "...",
            str(action)[:50]
        )

    console.print(table)
```

### logger.py - 日志保存

```python
import json
from datetime import datetime
from pathlib import Path

def save_loop_log(history, fingerprint, cost_saved):
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
```

### exceptions.py - 异常定义

```python
class LoopDetectedError(Exception):
    """循环检测异常"""
    pass
```

---

## 4. 使用示例

### 基础使用
```python
from loop_fuse import loop_fuse

@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    print(f"执行操作: {action}")
    return f"完成: {action}"

actions = ["搜索天气", "搜索新闻", "搜索新闻", "搜索新闻"]
for action in actions:
    agent_loop(action)  # 第 4 次会触发熔断
```

### 自定义回调
```python
def my_callback(history, fingerprint, cost_saved):
    print(f"[回调] 检测到循环！节省成本: ${cost_saved:.4f}")

@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    print(f"执行: {action}")
```

### 成本估算
```python
@loop_fuse(threshold=3, cost_per_call=0.01)
def expensive_agent_call(query):
    print(f"调用 API: {query}")
    return f"结果: {query}"
```

---

## 5. 测试策略

### 核心逻辑测试
- 测试基础循环检测
- 测试滚动窗口机制
- 测试不同操作不触发熔断

### 装饰器测试
- 测试装饰器基础功能
- 测试装饰器回调机制

### 指纹生成测试
- 测试相同字符串生成相同指纹
- 测试不同字符串生成不同指纹
- 测试字典类型指纹生成

---

## 6. 技术选型理由

### 为什么选择装饰器模式？
- 简单直观，符合 Python 开发者习惯
- 一行代码即可为函数添加循环检测
- 不侵入原有代码逻辑

### 为什么选择 MD5 哈希？
- 快速高效，适合实时检测
- 对于循环检测场景，碰撞概率可接受
- 无需引入额外依赖

### 为什么选择 rich 库？
- 提供美观的终端输出
- 支持表格、面板等丰富组件
- 广泛使用，稳定可靠

---

## 7. 未来扩展方向

- 支持语义相似度检测（使用 embedding）
- 支持 Web 仪表盘可视化
- 支持邮件/Slack 通知
- 支持更复杂的循环模式检测（如 A→B→A 模式）
