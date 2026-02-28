# loop-fuse 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个轻量级的 Python 循环检测和熔断库，使用装饰器模式为 AI Agent 提供死循环保护

**Architecture:** 使用滚动窗口 + MD5 哈希指纹检测重复操作，达到阈值时抛出异常并触发可视化警告、日志保存和自定义回调

**Tech Stack:** Python 3.8+, rich (终端可视化), hashlib (哈希), pytest (测试)

---

## Task 1: 项目基础结构

**Files:**
- Create: `src/loop_fuse/__init__.py`
- Create: `src/loop_fuse/exceptions.py`
- Create: `pyproject.toml`
- Create: `.gitignore`

**Step 1: 创建项目目录结构**

```bash
mkdir -p src/loop_fuse tests examples docs/plans
```

**Step 2: 创建异常类**

在 `src/loop_fuse/exceptions.py` 中：

```python
class LoopDetectedError(Exception):
    """循环检测异常"""
    pass
```

**Step 3: 创建 pyproject.toml**

```toml
[project]
name = "loop-fuse"
version = "0.1.0"
description = "循环检测和熔断器，防止 AI Agent 陷入死循环"
requires-python = ">=3.8"
dependencies = [
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

**Step 4: 创建 .gitignore**

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.pytest_cache/
.coverage
.loop-fuse-logs/
```

**Step 5: 初始化 git 并提交**

```bash
git init
git add .
git commit -m "chore: 初始化项目结构

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 指纹生成模块

**Files:**
- Create: `src/loop_fuse/fingerprint.py`
- Create: `tests/test_fingerprint.py`

**Step 1: 编写指纹生成测试**

在 `tests/test_fingerprint.py` 中：

```python
from loop_fuse.fingerprint import generate_fingerprint

def test_same_string_same_fingerprint():
    """相同字符串生成相同指纹"""
    fp1 = generate_fingerprint("test")
    fp2 = generate_fingerprint("test")
    assert fp1 == fp2

def test_different_string_different_fingerprint():
    """不同字符串生成不同指纹"""
    fp1 = generate_fingerprint("test1")
    fp2 = generate_fingerprint("test2")
    assert fp1 != fp2

def test_dict_fingerprint():
    """字典也能生成指纹"""
    fp = generate_fingerprint({"action": "search", "query": "test"})
    assert isinstance(fp, str)
    assert len(fp) == 32  # MD5 长度
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_fingerprint.py -v
```

预期: FAIL (模块不存在)

**Step 3: 实现指纹生成**

在 `src/loop_fuse/fingerprint.py` 中：

```python
import hashlib
from typing import Any

def generate_fingerprint(action: Any) -> str:
    """生成操作指纹（MD5 哈希）"""
    action_str = str(action)
    return hashlib.md5(action_str.encode('utf-8')).hexdigest()
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_fingerprint.py -v
```

预期: PASS (3 个测试通过)

**Step 5: 提交**

```bash
git add src/loop_fuse/fingerprint.py tests/test_fingerprint.py
git commit -m "feat: 添加指纹生成模块

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 核心 LoopFuse 类

**Files:**
- Create: `src/loop_fuse/core.py`
- Create: `tests/test_core.py`

**Step 1: 编写核心逻辑测试**

在 `tests/test_core.py` 中：

```python
import pytest
from loop_fuse.core import LoopFuse
from loop_fuse.exceptions import LoopDetectedError

def test_basic_loop_detection():
    """测试基础循环检测"""
    fuse = LoopFuse(window_size=5, threshold=3)

    fuse.monitor("action1")
    fuse.monitor("action1")

    with pytest.raises(LoopDetectedError):
        fuse.monitor("action1")

def test_window_size():
    """测试滚动窗口"""
    fuse = LoopFuse(window_size=3, threshold=2)

    fuse.monitor("a")
    fuse.monitor("b")
    fuse.monitor("c")
    fuse.monitor("a")

    with pytest.raises(LoopDetectedError):
        fuse.monitor("a")

def test_different_actions():
    """测试不同操作不触发"""
    fuse = LoopFuse(threshold=3)

    fuse.monitor("action1")
    fuse.monitor("action2")
    fuse.monitor("action3")
    fuse.monitor("action4")
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_core.py -v
```

预期: FAIL (模块不存在)

**Step 3: 实现核心类（最小实现）**

在 `src/loop_fuse/core.py` 中：

```python
from collections import deque
from typing import Any, Callable, Optional
from .fingerprint import generate_fingerprint
from .exceptions import LoopDetectedError

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

        raise LoopDetectedError(
            f"循环检测到！指纹 {fingerprint[:8]} 重复 {self.threshold} 次"
        )
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_core.py -v
```

预期: PASS (3 个测试通过)

**Step 5: 提交**

```bash
git add src/loop_fuse/core.py tests/test_core.py
git commit -m "feat: 添加核心 LoopFuse 类

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 可视化输出模块

**Files:**
- Create: `src/loop_fuse/ui.py`

**Step 1: 实现可视化输出**

在 `src/loop_fuse/ui.py` 中：

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import List, Tuple

def display_circuit_break_warning(
    history: List[Tuple[str, any]],
    fingerprint: str,
    cost_saved: float
) -> None:
    """显示熔断警告"""
    console = Console()

    repeat_count = sum(1 for fp, _ in history if fp == fingerprint)

    warning_text = f"""[bold red]⚠️  循环检测！系统已熔断 ⚠️[/bold red]

指纹: {fingerprint[:16]}...
重复次数: {repeat_count}
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

**Step 2: 集成到核心类**

修改 `src/loop_fuse/core.py` 的 `_trigger_circuit_break` 方法：

```python
from .ui import display_circuit_break_warning

def _trigger_circuit_break(self, fingerprint: str, action: Any) -> None:
    """触发熔断机制"""
    cost_saved = self.cost_per_call * (self.call_count - len(self.history))

    if self.on_loop_detected:
        self.on_loop_detected(list(self.history), fingerprint, cost_saved)

    display_circuit_break_warning(list(self.history), fingerprint, cost_saved)

    raise LoopDetectedError(
        f"循环检测到！指纹 {fingerprint[:8]} 重复 {self.threshold} 次"
    )
```

**Step 3: 手动测试可视化**

创建临时测试文件 `test_ui_manual.py`：

```python
from loop_fuse import LoopFuse

fuse = LoopFuse(threshold=3)
try:
    for i in range(5):
        fuse.monitor("重复操作")
except Exception as e:
    print(f"捕获异常: {e}")
```

运行: `python test_ui_manual.py`

预期: 显示红色警告面板和循环历史表格

**Step 4: 提交**

```bash
git add src/loop_fuse/ui.py src/loop_fuse/core.py
git commit -m "feat: 添加可视化输出模块

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: 日志保存模块

**Files:**
- Create: `src/loop_fuse/logger.py`

**Step 1: 实现日志保存**

在 `src/loop_fuse/logger.py` 中：

```python
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
```

**Step 2: 集成到核心类**

修改 `src/loop_fuse/core.py` 的 `_trigger_circuit_break` 方法：

```python
from .logger import save_loop_log

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
```

**Step 3: 手动测试日志保存**

运行之前的测试文件: `python test_ui_manual.py`

检查: `ls .loop-fuse-logs/`

预期: 生成 `loop_YYYYMMDD_HHMMSS.json` 文件

**Step 4: 提交**

```bash
git add src/loop_fuse/logger.py src/loop_fuse/core.py
git commit -m "feat: 添加日志保存模块

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: 装饰器模块

**Files:**
- Create: `src/loop_fuse/decorators.py`
- Create: `tests/test_decorators.py`

**Step 1: 编写装饰器测试**

在 `tests/test_decorators.py` 中：

```python
import pytest
from loop_fuse.decorators import loop_fuse
from loop_fuse.exceptions import LoopDetectedError

def test_decorator_basic():
    """测试装饰器基础功能"""
    @loop_fuse(threshold=2)
    def my_func(action):
        return action

    my_func("test")

    with pytest.raises(LoopDetectedError):
        my_func("test")

def test_decorator_with_callback():
    """测试装饰器回调"""
    callback_called = []

    def callback(history, fp, cost):
        callback_called.append(True)

    @loop_fuse(threshold=2, on_loop_detected=callback)
    def my_func(action):
        return action

    with pytest.raises(LoopDetectedError):
        my_func("test")

    assert len(callback_called) == 1
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_decorators.py -v
```

预期: FAIL (模块不存在)

**Step 3: 实现装饰器**

在 `src/loop_fuse/decorators.py` 中：

```python
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
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_decorators.py -v
```

预期: PASS (2 个测试通过)

**Step 5: 提交**

```bash
git add src/loop_fuse/decorators.py tests/test_decorators.py
git commit -m "feat: 添加装饰器模块

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: 暴露公共 API

**Files:**
- Modify: `src/loop_fuse/__init__.py`

**Step 1: 更新 __init__.py**

在 `src/loop_fuse/__init__.py` 中：

```python
"""loop-fuse: 循环检测和熔断器，防止 AI Agent 陷入死循环"""

from .core import LoopFuse
from .decorators import loop_fuse
from .exceptions import LoopDetectedError

__version__ = "0.1.0"
__all__ = ["LoopFuse", "loop_fuse", "LoopDetectedError"]
```

**Step 2: 测试导入**

```bash
python -c "from loop_fuse import LoopFuse, loop_fuse, LoopDetectedError; print('导入成功')"
```

预期: 输出 "导入成功"

**Step 3: 提交**

```bash
git add src/loop_fuse/__init__.py
git commit -m "feat: 暴露公共 API

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: 示例代码

**Files:**
- Create: `examples/basic_usage.py`
- Create: `examples/with_callback.py`
- Create: `examples/cost_estimation.py`

**Step 1: 创建基础使用示例**

在 `examples/basic_usage.py` 中：

```python
from loop_fuse import loop_fuse

@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    """模拟 Agent 循环"""
    print(f"执行操作: {action}")
    return f"完成: {action}"

if __name__ == "__main__":
    actions = ["搜索天气", "搜索新闻", "搜索新闻", "搜索新闻"]

    try:
        for action in actions:
            agent_loop(action)
    except Exception as e:
        print(f"\n捕获异常: {e}")
```

**Step 2: 创建回调示例**

在 `examples/with_callback.py` 中：

```python
from loop_fuse import loop_fuse

def my_callback(history, fingerprint, cost_saved):
    """自定义熔断回调"""
    print(f"\n[回调] 检测到循环！")
    print(f"[回调] 节省成本: ${cost_saved:.4f}")

@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    print(f"执行: {action}")

if __name__ == "__main__":
    try:
        for i in range(5):
            agent_loop("重复操作")
    except Exception as e:
        print(f"\n捕获异常: {e}")
```

**Step 3: 创建成本估算示例**

在 `examples/cost_estimation.py` 中：

```python
from loop_fuse import loop_fuse

@loop_fuse(threshold=3, cost_per_call=0.01)
def expensive_agent_call(query):
    """模拟昂贵的 API 调用"""
    print(f"调用 API: {query}")
    return f"结果: {query}"

if __name__ == "__main__":
    try:
        for i in range(10):
            expensive_agent_call("相同的查询")
    except Exception as e:
        print(f"\n捕获异常: {e}")
```

**Step 4: 测试所有示例**

```bash
python examples/basic_usage.py
python examples/with_callback.py
python examples/cost_estimation.py
```

预期: 所有示例都能正常运行并显示熔断警告

**Step 5: 提交**

```bash
git add examples/
git commit -m "docs: 添加使用示例

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 9: README 文档

**Files:**
- Create: `README.md`

**Step 1: 创建 README**

在 `README.md` 中：

```markdown
# loop-fuse

> 循环检测和熔断器，防止 AI Agent 陷入死循环

## 特性

- 🛡️ **装饰器模式** - 一行代码为函数添加循环检测
- 🔍 **智能检测** - 使用滚动窗口 + 哈希指纹检测重复操作
- 🚨 **可视化警告** - 使用 rich 库显示红色警告和循环历史
- 💾 **自动日志** - 熔断时自动保存日志到 `.loop-fuse-logs/`
- 💰 **成本估算** - 显示节省的 API 调用成本
- 🔧 **自定义回调** - 支持自定义熔断处理逻辑

## 安装

```bash
pip install loop-fuse
```

## 快速开始

```python
from loop_fuse import loop_fuse

@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    print(f"执行操作: {action}")
    return f"完成: {action}"

# 模拟死循环
actions = ["搜索天气", "搜索新闻", "搜索新闻", "搜索新闻"]
for action in actions:
    agent_loop(action)  # 第 4 次会触发熔断
```

## 使用场景

### 基础使用

```python
@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    # Agent 逻辑
    pass
```

### 成本估算

```python
@loop_fuse(threshold=3, cost_per_call=0.01)
def expensive_agent_call(query):
    # 昂贵的 API 调用
    pass
```

### 自定义回调

```python
def my_callback(history, fingerprint, cost_saved):
    # 自定义处理逻辑
    print(f"节省成本: ${cost_saved:.4f}")

@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    pass
```

## 参数说明

- `window_size` (int): 滚动窗口大小，默认 5
- `threshold` (int): 重复次数阈值，默认 3
- `cost_per_call` (float): 每次调用成本（美元），默认 0.0
- `on_loop_detected` (Callable): 自定义熔断回调函数

## 工作原理

1. 使用滚动窗口记录最近 N 次操作
2. 为每次操作生成 MD5 哈希指纹
3. 检测窗口内重复次数是否达到阈值
4. 触发熔断：显示警告 + 保存日志 + 抛出异常

## 许可证

MIT
```

**Step 2: 提交**

```bash
git add README.md
git commit -m "docs: 添加 README 文档

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 10: 运行完整测试

**Step 1: 安装依赖**

```bash
pip install -e ".[dev]"
```

**Step 2: 运行所有测试**

```bash
pytest tests/ -v --cov=src/loop_fuse
```

预期: 所有测试通过，覆盖率 > 80%

**Step 3: 运行示例验证**

```bash
python examples/basic_usage.py
python examples/with_callback.py
python examples/cost_estimation.py
```

预期: 所有示例正常运行

**Step 4: 最终提交**

```bash
git add .
git commit -m "chore: 完成 loop-fuse MVP 实现

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 完成标准

- ✅ 所有测试通过
- ✅ 代码覆盖率 > 80%
- ✅ 所有示例可运行
- ✅ README 文档完整
- ✅ 设计文档已保存

## 后续优化（可选）

- 添加 CI/CD 配置
- 发布到 PyPI
- 添加更多测试用例
- 支持语义相似度检测
