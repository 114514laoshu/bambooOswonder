# Contributing to Bamboo OS Wonder Series

# 贡献指南

First off, thank you for considering contributing to Bamboo OS! It's people like you that make Bamboo OS such a great tool.

首先，感谢您考虑为 Bamboo OS 做贡献！正是像您这样的人让 Bamboo OS 成为如此出色的工具。

## Code of Conduct / 行为准则

This project and everyone participating in it is governed by the Bamboo OS Code of Conduct. By participating, you are expected to uphold this code.

本项目及其所有参与者都受 Bamboo OS 行为准则的约束。通过参与，您需要遵守此准则。

## How Can I Contribute? / 我如何贡献？

### Reporting Bugs / 报告 Bug

This section guides you through submitting a bug report for Bamboo OS. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

本节指导您如何提交 Bamboo OS 的 bug 报告。遵循这些指南有助于维护者和社区理解您的报告、复现行为并找到相关报告。

**Before submitting a bug report / 提交 bug 报告前:**

- Check the [documentation](docs/) for FAQs / 查看文档中的常见问题
- Check the [issues](https://github.com/) for existing reports / 查看现有问题报告
- Ensure you're using the latest version / 确保使用最新版本

**How to submit a good bug report / 如何提交好的 bug 报告:**

- Use a clear and descriptive title / 使用清晰描述性的标题
- Describe the exact steps to reproduce the problem / 描述复现问题的确切步骤
- Provide specific examples to demonstrate the steps / 提供具体示例来演示步骤
- Describe the behavior you observed after following the steps / 描述遵循步骤后观察到的行为
- Explain which behavior you expected to see instead and why / 解释您期望看到的行为及原因
- Include system details (OS, Python version, etc.) / 包含系统详情（操作系统、Python 版本等）

### Suggesting Enhancements / 建议增强功能

This section guides you through submitting an enhancement suggestion for Bamboo OS, including completely new features and minor improvements to existing functionality.

本节指导您如何提交 Bamboo OS 的增强功能建议，包括全新功能和对现有功能的小改进。

**Before submitting enhancement suggestions / 提交增强建议前:**

- Check if the enhancement is already covered / 检查是否已涵盖该增强
- Check if there's already a suggestion / 检查是否已有建议

### Pull Requests / 拉取请求

The process described here has several goals:

这里描述的流程有几个目标：

- Maintain Bamboo OS's quality / 保持 Bamboo OS 的质量
- Fix problems that are important to users / 修复对用户重要的问题
- Engage the community in working toward the best possible Bamboo OS / 让社区参与打造最好的 Bamboo OS
- Enable a sustainable system for Bamboo OS's maintainers to review contributions / 为 Bamboo OS 维护者提供可持续的贡献审查系统

## Coding Standards / 编码标准

### Bilingual Comments / 双语言注释

All code must have English + Chinese comments:

所有代码必须包含英文+中文注释：

```python
# ============================================================================
# Module: example.py
# 模块：example.py
# Description: Example module for demonstration
# 描述：用于演示的示例模块
# ============================================================================

class ExampleClass:
    """
    Example class for demonstration.
    用于演示的示例类。

    This class shows the proper way to document code.
    该类展示了编写代码文档的正确方式。
    """

    def example_method(self, param):
        """
        Example method with proper documentation.
        带有正确文档的示例方法。

        Args:
            参数：
            param (int): Description of parameter / 参数描述

        Returns:
            返回：
            bool: Description of return value / 返回值描述
        """
        return True
```

### Python Style / Python 风格

- Follow PEP 8 / 遵循 PEP 8
- Use 4 spaces for indentation / 使用 4 空格缩进
- Maximum line length: 120 characters / 最大行长度：120 字符
- Use meaningful variable names / 使用有意义的变量名
- Type hints are encouraged / 鼓励使用类型提示

### File Headers / 文件头

Every source file must start with:

每个源文件必须以以下内容开头：

```python
# ============================================================================
# Module: path/to/module.py
# 模块：path/to/module.py
# Description: Brief description of the module
# 描述：模块的简要描述
# ============================================================================
```

## Development Workflow / 开发流程

### Setting Up / 环境搭建

1. Fork the repository / Fork 仓库
2. Clone your fork / 克隆您的 fork
3. Create a feature branch / 创建功能分支
4. Make your changes / 进行修改
5. Test your changes / 测试修改
6. Submit a pull request / 提交拉取请求

### Branch Naming / 分支命名

- `feature/xxx` for new features / 新功能
- `bugfix/xxx` for bug fixes / Bug 修复
- `docs/xxx` for documentation / 文档
- `refactor/xxx` for refactoring / 重构

### Commit Messages / 提交信息

Use clear and descriptive commit messages:

使用清晰描述性的提交信息：

```
feat: add new GUI widget library
fix: resolve memory leak in scheduler
docs: update build guide for Windows
refactor: reorganize kernel memory management
```

## Testing / 测试

Before submitting a PR, make sure:

提交 PR 前，请确保：

- [ ] Code builds successfully / 代码成功构建
- [ ] All existing tests pass / 所有现有测试通过
- [ ] New features include tests / 新功能包含测试
- [ ] Documentation is updated / 文档已更新

### Running Tests / 运行测试

```bash
# Run all tests
python -m pytest tests/

# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/
```

### Build Verification / 构建验证

```bash
# Build all targets
python buildmain.py --target=all

# Validate build
python scripts/validate.py --target=all
```

## Pull Request Process / 拉取请求流程

1. Update the README.md / docs with details of changes to the interface / 更新 README.md/文档，说明接口变更
2. Update the documentation with any new functionality / 更新文档，添加任何新功能
3. The PR will be merged once reviewed and tested / PR 将在审查和测试通过后合并
4. At least one maintainer approval is required / 至少需要一名维护者批准

## Getting Help / 获取帮助

If you need help, feel free to:

如果您需要帮助，请随时：

- Open an issue / 开启一个 issue
- Ask in discussions / 在讨论中提问
- Check the documentation / 查看文档

## Recognition / 认可

Contributors will be recognized in:

贡献者将在以下地方获得认可：

- AUTHORS file / AUTHORS 文件
- Release notes / 发布说明
- Contributors page / 贡献者页面

Thank you for contributing to Bamboo OS!

感谢您为 Bamboo OS 做贡献！
