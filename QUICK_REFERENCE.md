# SEC Parser 快速参考指南

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 获取Apple最新财报
python3 -m sec_parser AAPL

# 验证数据
python3 verify_data.py AAPL_10-K_2025.xlsx 2025
```

## 📋 常用命令

### 获取财务数据

```bash
# 基本用法
python3 -m sec_parser <TICKER>

# 指定年份
python3 -m sec_parser AAPL --year 2024

# 获取季报
python3 -m sec_parser MSFT --form 10-Q

# 指定输出目录
python3 -m sec_parser GOOGL -o ./reports

# 详细日志
python3 -m sec_parser AMZN --verbose
```

### 验证数据

```bash
# 单文件验证
python3 verify_data.py <file.xlsx> <year>

# 批量验证
python3 batch_verify.py file1.xlsx file2.xlsx

# 验证目录下所有文件
python3 batch_verify.py --dir ./reports

# 详细分析
python3 detailed_analysis.py <file.xlsx>
```

## 📊 支持的公司示例

| 公司 | 代码 | 财年结束 |
|------|------|----------|
| Apple | AAPL | 9月 |
| Microsoft | MSFT | 6月 |
| Google | GOOGL | 12月 |
| Amazon | AMZN | 12月 |
| Meta | META | 12月 |
| Tesla | TSLA | 12月 |
| Visa | V | 9月 |
| Mastercard | MA | 12月 |
| NVIDIA | NVDA | 1月 |
| Intel | INTC | 12月 |

## 📁 输出文件结构

```
生成的Excel文件包含4个工作表：
├── Income Statement    (损益表)
├── Balance Sheet       (资产负债表)
├── Cash Flow          (现金流量表)
└── Segments           (分部信息)
```

## 🔍 验证状态说明

| 状态 | 说明 |
|------|------|
| ✅ PASSED | 所有数据与SEC官方数据一致 |
| ❌ FAILED | 发现数据差异 |
| ⚠️ ERROR | 验证过程出错 |

## 💡 使用技巧

### 1. 批量下载多家公司数据

```bash
#!/bin/bash
for ticker in AAPL MSFT GOOGL AMZN META; do
    python3 -m sec_parser $ticker --year 2025
done
```

### 2. 下载历史数据

```bash
#!/bin/bash
for year in 2023 2024 2025; do
    python3 -m sec_parser AAPL --year $year
done
```

### 3. 自动验证新下载的文件

```bash
# 下载并验证
python3 -m sec_parser AAPL --year 2025 && \
python3 verify_data.py AAPL_10-K_2025.xlsx 2025
```

### 4. 验证目录下所有文件

```bash
python3 batch_verify.py --dir .
```

## 🔧 故障排除

### 问题：找不到公司
```bash
# 确认股票代码正确
# 访问 https://www.sec.gov/edgar/searchedgar/companysearch.html
```

### 问题：验证失败
```bash
# 检查年份是否正确
python3 detailed_analysis.py <file.xlsx>

# 查看文件中的实际年份
```

### 问题：速率限制
```bash
# SEC限制每秒10个请求
# 工具已自动处理，如遇问题请稍后重试
```

## 📖 数据说明

### 金额单位
- **Excel显示**: 千（thousands）
- **原始数据**: 美元
- **示例**: Excel中的 100,000 = $100,000,000

### 财年 vs 日历年
- 文件名中的年份指**财年**
- Apple财年：9月结束（如FY2025 = 2024年10月-2025年9月）
- 大多数公司：12月结束（与日历年一致）

### 报告类型
- **10-K**: 年度报告（完整财务数据）
- **10-Q**: 季度报告（季度财务数据）

## 🔗 有用的链接

- **SEC EDGAR**: https://www.sec.gov/edgar
- **公司查询**: https://www.sec.gov/edgar/searchedgar/companysearch.html
- **API文档**: https://www.sec.gov/edgar/sec-api-documentation

## 📞 获取帮助

```bash
# 查看命令帮助
python3 -m sec_parser --help

# 查看详细文档
cat README.md
```

## ⚡ 快捷命令别名

添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
# SEC Parser 别名
alias sec-get='python3 -m sec_parser'
alias sec-verify='python3 verify_data.py'
alias sec-batch='python3 batch_verify.py'
alias sec-analyze='python3 detailed_analysis.py'
```

使用示例：
```bash
sec-get AAPL
sec-verify AAPL_10-K_2025.xlsx 2025
```

## 📈 常见工作流

### 工作流1: 获取并验证单个公司
```bash
python3 -m sec_parser AAPL --year 2025
python3 verify_data.py AAPL_10-K_2025.xlsx 2025
```

### 工作流2: 批量处理多个公司
```bash
# 下载
for t in AAPL MSFT GOOGL; do python3 -m sec_parser $t; done

# 验证
python3 batch_verify.py *.xlsx
```

### 工作流3: 历史数据分析
```bash
# 下载3年数据
for y in 2023 2024 2025; do
    python3 -m sec_parser AAPL --year $y
done

# 在Excel中打开进行对比分析
```

---

**提示**: 将此文件保存为书签，随时查阅！
