# 🚀 金融借款系统接口自动化测试框架

## 🌟 项目简介
基于Python+Pytest构建的金融风控系统接口自动化测试框架，支持贷款、还款、风控等核心业务流程的自动化测试。

## 🛠️ 主要功能
| 功能模块 | 描述 |
|---------|------|
| **核心接口测试** | 支持贷款、还款、风控等业务流程测试 |
| **数据库验证** | 自动验证数据库操作结果 |
| **数据加密** | 支持敏感数据加密解密 |
| **测试数据生成** | 自动生成测试数据 |
| **性能测试** | 支持接口性能测试 |
| **测试报告** | 生成HTML格式测试报告 |

## 📂 项目结构
```bash
├── common/            # 核心接口模块
│   ├── Core_Api_Flow_Api.py  # 业务流程API
│   ├── Core_Risk_API.py      # 风控API
│   └── ...
├── testcase/          # 测试用例
│   ├── test_tyh_api_flow/    # 同花API测试
│   └── test_zjly/           # 资金流测试
├── util_tools/        # 实用工具
│   ├── Database_Conn.py     # 数据库连接
│   ├── Redis_Conn.py        # Redis连接
│   └── ...
└── ...
```

## 🚀 快速开始
### 环境准备
1. 安装Python 3.8+
2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 运行测试
```bash
# 运行所有测试
pytest testcase/

# 运行特定模块测试
pytest testcase/test_zjly/
```

### 查看报告
测试完成后，打开`report/html/index.html`查看测试报告

## 🤝 贡献指南
欢迎通过Pull Request贡献代码，请遵循以下规范：
1. 创建功能分支
2. 添加清晰的提交信息
3. 更新相关文档

## 📞 联系方式
如有问题，请联系项目负责人
