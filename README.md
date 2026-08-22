# loop-fuse
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/loop-fuse)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A lightweight circuit breaker for AI Agents to prevent infinite loops

> 一个轻量级的 AI Agent 循环检测和熔断库，防止陷入死循环

---

## Features | 特性

- 🛡️ **Decorator Pattern** - Add loop detection with a single line of code | 装饰器模式 - 一行代码添加循环检测
- 🔍 **Smart Detection** - Uses sliding window + MD5 fingerprint to detect repeated operations | 智能检测 - 使用滚动窗口 + MD5 哈希指纹检测重复操作
- 🚨 **Visual Warnings** - Rich terminal UI with red alerts and loop history | 可视化警告 - 使用 rich 库显示红色警告和循环历史
- 💾 **Auto Logging** - Automatically saves logs to `.loop-fuse-logs/` on circuit break | 自动日志 - 熔断时自动保存日志
- 💰 **Cost Estimation** - Shows saved API call costs | 成本估算 - 显示节省的 API 调用成本
- 🔧 **Custom Callbacks** - Support for custom circuit break handlers | 自定义回调 - 支持自定义熔断处理逻辑

---

## Quick Start | 快速开始

### Installation | 安装

```bash
pip install loop-fuse
```

### Basic Usage | 基础使用

```python
from loop_fuse import loop_fuse

@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    print(f"Executing: {action}")
    return f"Completed: {action}"

# Simulate infinite loop | 模拟死循环
actions = ["search weather", "search news", "search news", "search news"]
for action in actions:
    agent_loop(action)  # Will trigger circuit break on 4th call | 第 4 次会触发熔断
```

---

## Usage Guide | 使用指南

### Basic Loop Detection | 基础循环检测

```python
@loop_fuse(window_size=5, threshold=3)
def agent_loop(action):
    # Your agent logic here
    pass
```

### Cost Estimation | 成本估算

```python
@loop_fuse(threshold=3, cost_per_call=0.01)
def expensive_agent_call(query):
    # Expensive API call (e.g., GPT-4)
    pass
```

### Custom Callbacks | 自定义回调

```python
def my_callback(history, fingerprint, cost_saved):
    # Custom handling logic
    print(f"Saved cost: ${cost_saved:.4f}")

@loop_fuse(threshold=3, on_loop_detected=my_callback)
def agent_loop(action):
    pass
```

### Parameters | 参数说明

- `window_size` (int): Sliding window size, default 5 | 滚动窗口大小，默认 5
- `threshold` (int): Repetition threshold, default 3 | 重复次数阈值，默认 3
- `cost_per_call` (float): Cost per call in USD, default 0.0 | 每次调用成本（美元），默认 0.0
- `on_loop_detected` (Callable): Custom circuit break callback | 自定义熔断回调函数

---

## Project Structure | 项目结构

```
loop-fuse/
├── src/loop_fuse/
│   ├── __init__.py          # Public API
│   ├── core.py              # Core LoopFuse class
│   ├── decorators.py        # @loop_fuse decorator
│   ├── fingerprint.py       # MD5 fingerprint generation
│   ├── exceptions.py        # LoopDetectedError exception
│   ├── logger.py            # JSON log saving
│   └── ui.py                # Rich visual output
├── examples/
│   ├── basic_usage.py       # Basic usage example
│   ├── with_callback.py     # Custom callback example
│   └── cost_estimation.py   # Cost estimation example
├── tests/
│   ├── test_core.py         # Core logic tests
│   ├── test_decorators.py   # Decorator tests
│   └── test_fingerprint.py  # Fingerprint generation tests
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── pyproject.toml
```

---

## How It Works | 工作原理

1. Uses a sliding window to record the last N operations | 使用滚动窗口记录最近 N 次操作
2. Generates MD5 hash fingerprint for each operation | 为每次操作生成 MD5 哈希指纹
3. Detects if repetition count within window exceeds threshold | 检测窗口内重复次数是否达到阈值
4. Triggers circuit break: displays warning + saves log + raises exception | 触发熔断：显示警告 + 保存日志 + 抛出异常

---

## Tech Stack | 技术栈

- **Python 3.8+** - Base runtime environment | 基础运行环境
- **rich** - Terminal visualization | 终端可视化输出
- **hashlib** - MD5 hash generation (built-in) | MD5 哈希生成（内置库）
- **pytest** - Unit testing framework | 单元测试框架
- **pytest-cov** - Test coverage | 测试覆盖率

---

## Development | 开发

### Install Dependencies | 安装依赖

```bash
pip install -e ".[dev]"
```

### Run Tests | 运行测试

```bash
pytest tests/ -v --cov=src/loop_fuse
```

### Run Examples | 运行示例

```bash
python examples/basic_usage.py
python examples/with_callback.py
python examples/cost_estimation.py
```

---

## Contributing | 贡献

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

---

## License | 许可证

Apache License 2.0

Copyright 2026 Chance Dean (novelnexusai@outlook.com)

See [LICENSE](LICENSE) file for details.

查看 [LICENSE](LICENSE) 文件了解详情。

---

## Author | 作者

**Chance Dean** ([@PerryLink](https://github.com/PerryLink))

- Email: novelnexusai@outlook.com
- GitHub: https://github.com/PerryLink

---

## Acknowledgments | 致谢

Built with ❤️ to help AI developers avoid infinite loops and save API costs.

用 ❤️ 构建，帮助 AI 开发者避免死循环并节省 API 成本。
