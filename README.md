# SEC Filing Parser & Verifier

自动从SEC官网获取上市公司财务数据，导出为Excel格式，并提供数据验证功能。

## 功能特性

- 📊 **自动获取财务数据**: 从SEC EDGAR API获取10-K/10-Q报告数据
- 📈 **三大财务报表**: 损益表、资产负债表、现金流量表
- 📑 **Excel导出**: 格式化的Excel文件，便于分析
- ✅ **数据验证**: 验证Excel文件数据与SEC官方数据的一致性
- 🔍 **多年度支持**: 可获取历史多年财务数据

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包：
- `requests` - HTTP请求
- `pandas` - 数据处理
- `openpyxl` - Excel文件操作
- `lxml` - XML解析

## 使用方法

### 1. 获取财务数据并导出Excel

```bash
# 获取Apple最新的10-K报告
python3 -m sec_parser AAPL

# 获取Microsoft最新的10-Q报告
python3 -m sec_parser MSFT --form 10-Q

# 获取Google 2023年的10-K报告
python3 -m sec_parser GOOGL --year 2023

# 指定输出目录
python3 -m sec_parser AMZN -o ./reports

# 显示详细日志
python3 -m sec_parser AAPL --verbose
```

#### 参数说明

- `ticker`: 股票代码（必需）
- `--form, -f`: 报告类型，10-K（年报）或10-Q（季报），默认10-K
- `--year, -y`: 财年，默认最新
- `--output, -o`: 输出目录，默认当前目录
- `--verbose, -v`: 显示详细日志

### 2. 验证Excel文件数据

验证Excel文件中的数据是否与SEC官方数据一致：

```bash
# 验证Apple 2025年数据
python3 verify_data.py AAPL_10-K_2025.xlsx 2025

# 验证Visa 2025年数据
python3 verify_data.py V_10-K_2025.xlsx 2025
```

验证脚本会：
- 从SEC官网获取最新数据
- 逐项比对Excel中的数据
- 显示匹配/不匹配的项目
- 生成验证报告

### 3. 详细分析

查看Excel文件包含的数据和对应的SEC备案信息：

```bash
python3 detailed_analysis.py AAPL_10-K_2025.xlsx
```

## 输出文件格式

生成的Excel文件包含以下工作表：

### 1. Income Statement (损益表)
- 收入 (Revenue)
- 营业成本 (Cost of Revenue)
- 毛利润 (Gross Profit)
- 研发费用 (R&D)
- 销售及管理费用 (SG&A)
- 营业利润 (Operating Income)
- 净利润 (Net Income)
- 每股收益 (EPS)

### 2. Balance Sheet (资产负债表)
- **资产**
  - 流动资产（现金、应收账款、存货等）
  - 非流动资产（固定资产、商誉、无形资产等）
- **负债**
  - 流动负债（应付账款、短期债务等）
  - 长期负债
- **股东权益**
  - 普通股
  - 留存收益
  - 其他综合收益

### 3. Cash Flow (现金流量表)
- **经营活动**
  - 净利润
  - 折旧摊销
  - 营运资本变化
- **投资活动**
  - 资本支出
  - 投资购买/出售
- **融资活动**
  - 债务发行/偿还
  - 股票回购
  - 股息支付

### 4. Segments (分部信息)
- 业务分部
- 地理分部

## 项目结构

```
ggfunny/
├── sec_parser/              # SEC解析器核心模块
│   ├── __init__.py
│   ├── __main__.py         # CLI入口
│   ├── client.py           # SEC API客户端
│   ├── extractor.py        # 财务数据提取器
│   ├── excel_exporter.py   # Excel导出器
│   ├── models.py           # 数据模型
│   └── mappings.py         # XBRL标签映射
├── verify_data.py          # 数据验证脚本
├── detailed_analysis.py    # 详细分析脚本
├── requirements.txt        # Python依赖
├── verification_report.md  # 验证报告
└── README.md              # 本文档
```

## 数据来源

所有数据来自SEC官方EDGAR系统：

- **API端点**: https://data.sec.gov/api/xbrl/companyfacts/
- **数据格式**: XBRL (eXtensible Business Reporting Language)
- **标准**: US-GAAP (美国通用会计准则)

### 数据追溯

每个公司的数据都可以通过CIK号追溯到SEC官方来源：

- Apple (CIK: 0000320193): https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
- Visa (CIK: 0001403161): https://data.sec.gov/api/xbrl/companyfacts/CIK0001403161.json

## 验证报告

已验证的文件：

| 公司 | 文件名 | 财年 | 验证状态 | 匹配项 |
|------|--------|------|----------|--------|
| Apple Inc. | AAPL_10-K_2025.xlsx | 2025 | ✅ 通过 | 53/53 |
| Visa Inc. | V_10-K_2025.xlsx | 2025 | ✅ 通过 | 49/49 |

详细验证报告见：[verification_report.md](verification_report.md)

## 使用示例

### 示例1: 获取并验证Apple财务数据

```bash
# 1. 获取数据
python3 -m sec_parser AAPL --year 2025

# 2. 验证数据
python3 verify_data.py AAPL_10-K_2025.xlsx 2025

# 输出: ✅ All data verified successfully!
```

### 示例2: 批量获取多家公司数据

```bash
# 获取科技巨头财务数据
for ticker in AAPL MSFT GOOGL AMZN META; do
    python3 -m sec_parser $ticker --year 2025 -o ./tech_companies
done
```

### 示例3: 获取历史数据对比

```bash
# 获取Apple近3年数据
python3 -m sec_parser AAPL --year 2025
python3 -m sec_parser AAPL --year 2024
python3 -m sec_parser AAPL --year 2023
```

## 注意事项

### SEC API限制

- **速率限制**: 每秒最多10个请求
- **User-Agent**: 必须提供有效的User-Agent头
- 本工具已自动处理速率限制

### 数据精度

- 金额单位：千（thousands）
- EPS单位：美元
- 股数单位：千股

### 财年vs日历年

注意区分财年和日历年：
- Apple财年结束于9月
- Visa财年结束于9月
- 文件名中的年份指财年，非日历年

## 常见问题

### Q: 如何查找公司的股票代码？
A: 访问 https://www.sec.gov/edgar/searchedgar/companysearch.html

### Q: 为什么有些数据项为空？
A: 不同公司的财务报表结构不同，某些XBRL标签可能不适用于特定公司。

### Q: 如何获取季度报告？
A: 使用 `--form 10-Q` 参数获取季度报告（10-Q）。

### Q: 数据更新频率？
A: SEC数据实时更新，公司提交报告后立即可用。

### Q: 支持哪些公司？
A: 所有在SEC注册的美国上市公司（包括外国公司的ADR）。

## 技术细节

### XBRL标签映射

本工具使用US-GAAP标准XBRL标签，主要标签包括：

- `Revenues` / `RevenueFromContractWithCustomerExcludingAssessedTax`
- `CostOfRevenue`
- `GrossProfit`
- `ResearchAndDevelopmentExpense`
- `SellingGeneralAndAdministrativeExpense`
- `OperatingIncomeLoss`
- `NetIncomeLoss`
- `EarningsPerShareBasic` / `EarningsPerShareDiluted`

完整映射见：`sec_parser/mappings.py`

### 数据提取逻辑

1. 通过ticker查找CIK号
2. 获取公司所有XBRL facts
3. 根据财年和报告类型筛选数据
4. 匹配XBRL标签到财务报表项目
5. 格式化并导出到Excel

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。

---

**最后更新**: 2026-02-01
**版本**: 1.0.0
