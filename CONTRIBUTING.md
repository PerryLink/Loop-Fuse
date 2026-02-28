# Contributing to loop-fuse

## Project Status | 项目状态

This is a personal project currently maintained by [@PerryLink](https://github.com/PerryLink). While contributions are welcome, please note that this project is primarily developed and maintained by a single developer.

这是一个个人项目，目前由 [@PerryLink](https://github.com/PerryLink) 维护。虽然欢迎贡献，但请注意这个项目主要由单个开发者开发和维护。

---

## How to Report Issues | 如何报告问题

If you encounter a bug or have a feature request, please:

如果你遇到 bug 或有功能请求，请：

1. **Search existing issues** - Check if the issue has already been reported

   **搜索现有问题** - 检查问题是否已被报告

2. **Create a new issue** - If not found, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Python version and environment details

   **创建新问题** - 如果没有找到，创建新问题并包含：
   - 清晰的标题和描述
   - 重现步骤（针对 bug）
   - 期望行为 vs 实际行为
   - Python 版本和环境详情

---

## Development Environment Setup | 开发环境搭建

### Prerequisites | 前置要求

- Python 3.8 or higher | Python 3.8 或更高版本
- Git

### Setup Steps | 搭建步骤

1. **Fork and clone the repository | Fork 并克隆仓库**

```bash
git clone https://github.com/PerryLink/loop-fuse.git
cd loop-fuse
```

2. **Create a virtual environment | 创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies | 安装依赖**

```bash
pip install -e ".[dev]"
```

4. **Run tests to verify setup | 运行测试验证安装**

```bash
pytest tests/ -v --cov=src/loop_fuse
```

---

## Code Standards | 代码规范

### PEP 8 Compliance | PEP 8 合规

This project follows [PEP 8](https://peps.python.org/pep-0008/) style guidelines:

本项目遵循 [PEP 8](https://peps.python.org/pep-0008/) 风格指南：

- Use 4 spaces for indentation (no tabs) | 使用 4 个空格缩进（不使用制表符）
- Maximum line length: 88 characters (Black default) | 最大行长度：88 字符（Black 默认）
- Use descriptive variable names | 使用描述性变量名
- Add docstrings for public functions and classes | 为公共函数和类添加文档字符串

### Code Formatting | 代码格式化

We recommend using [Black](https://github.com/psf/black) for automatic formatting:

我们推荐使用 [Black](https://github.com/psf/black) 进行自动格式化：

```bash
pip install black
black src/ tests/
```

### Testing | 测试

- Write unit tests for new features | 为新功能编写单元测试
- Ensure all tests pass before submitting PR | 提交 PR 前确保所有测试通过
- Maintain or improve code coverage | 保持或提高代码覆盖率

```bash
pytest tests/ -v --cov=src/loop_fuse --cov-report=html
```

---

## Pull Request Process | 提交 Pull Request 流程

1. **Create a feature branch | 创建功能分支**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes | 进行修改**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

   - 编写清晰、有文档的代码
   - 为新功能添加测试
   - 如需要更新文档

3. **Run tests and formatting | 运行测试和格式化**

```bash
black src/ tests/
pytest tests/ -v --cov=src/loop_fuse
```

4. **Commit your changes | 提交更改**

```bash
git add .
git commit -m "feat: add your feature description"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 格式：
- `feat:` - 新功能
- `fix:` - Bug 修复
- `docs:` - 文档更改
- `test:` - 测试添加或更改
- `refactor:` - 代码重构

5. **Push to your fork | 推送到你的 fork**

```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request | 创建 Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with:
     - Description of changes
     - Related issue number (if applicable)
     - Testing performed

   - 前往原始仓库
   - 点击 "New Pull Request"
   - 选择你的分支
   - 填写 PR 模板，包含：
     - 更改描述
     - 相关问题编号（如适用）
     - 执行的测试

---

## Questions? | 有问题？

Feel free to open an issue for any questions or reach out to:

随时开启 issue 提问或联系：

- **Email | 邮箱**: novelnexusai@outlook.com
- **GitHub**: [@PerryLink](https://github.com/PerryLink)

---

## License | 许可证

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

通过贡献，你同意你的贡献将在 Apache License 2.0 下授权。
