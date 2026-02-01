"""US-GAAP XBRL tag mappings for financial statement extraction."""

# Income Statement tags (ordered by preference - most common first)
INCOME_STATEMENT_TAGS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "SalesRevenueGoodsNet",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
    ],
    "cost_of_revenue": [
        "CostOfGoodsAndServicesSold",
        "CostOfRevenue",
        "CostOfGoodsSold",
        "CostOfServices",
    ],
    "gross_profit": [
        "GrossProfit",
    ],
    "research_and_development": [
        "ResearchAndDevelopmentExpense",
        "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost",
    ],
    "selling_general_admin": [
        "SellingGeneralAndAdministrativeExpense",
        "SellingAndMarketingExpense",
        "GeneralAndAdministrativeExpense",
    ],
    "operating_expenses": [
        "OperatingExpenses",
        "CostsAndExpenses",
    ],
    "operating_income": [
        "OperatingIncomeLoss",
    ],
    "interest_expense": [
        "InterestExpense",
        "InterestExpenseDebt",
    ],
    "interest_income": [
        "InterestAndDividendIncomeOperating",
        "InvestmentIncomeInterest",
        "InterestIncomeOther",
    ],
    "other_income_expense": [
        "OtherNonoperatingIncomeExpense",
        "NonoperatingIncomeExpense",
    ],
    "income_before_tax": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
    ],
    "income_tax_expense": [
        "IncomeTaxExpenseBenefit",
    ],
    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
        "NetIncomeLossAvailableToCommonStockholdersBasic",
    ],
    "eps_basic": [
        "EarningsPerShareBasic",
    ],
    "eps_diluted": [
        "EarningsPerShareDiluted",
    ],
    "shares_basic": [
        "WeightedAverageNumberOfSharesOutstandingBasic",
    ],
    "shares_diluted": [
        "WeightedAverageNumberOfDilutedSharesOutstanding",
    ],
}

# Balance Sheet tags
BALANCE_SHEET_TAGS = {
    # Current Assets
    "cash_and_equivalents": [
        "CashAndCashEquivalentsAtCarryingValue",
        "Cash",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    "short_term_investments": [
        "ShortTermInvestments",
        "MarketableSecuritiesCurrent",
        "AvailableForSaleSecuritiesDebtSecuritiesCurrent",
    ],
    "accounts_receivable": [
        "AccountsReceivableNetCurrent",
        "ReceivablesNetCurrent",
    ],
    "inventory": [
        "InventoryNet",
        "InventoryFinishedGoodsAndWorkInProcess",
    ],
    "prepaid_expenses": [
        "PrepaidExpenseAndOtherAssetsCurrent",
        "PrepaidExpenseCurrent",
    ],
    "total_current_assets": [
        "AssetsCurrent",
    ],
    # Non-Current Assets
    "property_plant_equipment": [
        "PropertyPlantAndEquipmentNet",
    ],
    "goodwill": [
        "Goodwill",
    ],
    "intangible_assets": [
        "IntangibleAssetsNetExcludingGoodwill",
        "FiniteLivedIntangibleAssetsNet",
    ],
    "long_term_investments": [
        "LongTermInvestments",
        "MarketableSecuritiesNoncurrent",
    ],
    "other_assets": [
        "OtherAssetsNoncurrent",
    ],
    "total_assets": [
        "Assets",
    ],
    # Current Liabilities
    "accounts_payable": [
        "AccountsPayableCurrent",
    ],
    "accrued_liabilities": [
        "AccruedLiabilitiesCurrent",
        "EmployeeRelatedLiabilitiesCurrent",
    ],
    "deferred_revenue_current": [
        "DeferredRevenueCurrent",
        "ContractWithCustomerLiabilityCurrent",
    ],
    "short_term_debt": [
        "ShortTermBorrowings",
        "DebtCurrent",
    ],
    "current_portion_long_term_debt": [
        "LongTermDebtCurrent",
    ],
    "total_current_liabilities": [
        "LiabilitiesCurrent",
    ],
    # Non-Current Liabilities
    "long_term_debt": [
        "LongTermDebtNoncurrent",
        "LongTermDebt",
    ],
    "deferred_tax_liabilities": [
        "DeferredIncomeTaxLiabilitiesNet",
    ],
    "other_liabilities": [
        "OtherLiabilitiesNoncurrent",
    ],
    "total_liabilities": [
        "Liabilities",
    ],
    # Stockholders' Equity
    "common_stock": [
        "CommonStockValue",
        "CommonStocksIncludingAdditionalPaidInCapital",
    ],
    "additional_paid_in_capital": [
        "AdditionalPaidInCapitalCommonStock",
        "AdditionalPaidInCapital",
    ],
    "retained_earnings": [
        "RetainedEarningsAccumulatedDeficit",
    ],
    "accumulated_other_comprehensive_income": [
        "AccumulatedOtherComprehensiveIncomeLossNetOfTax",
    ],
    "treasury_stock": [
        "TreasuryStockValue",
    ],
    "total_stockholders_equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "total_liabilities_and_equity": [
        "LiabilitiesAndStockholdersEquity",
    ],
}

# Cash Flow Statement tags
CASH_FLOW_TAGS = {
    # Operating Activities
    "net_income_cf": [
        "NetIncomeLoss",
        "ProfitLoss",
    ],
    "depreciation_amortization": [
        "DepreciationDepletionAndAmortization",
        "DepreciationAndAmortization",
    ],
    "stock_based_compensation": [
        "ShareBasedCompensation",
        "AllocatedShareBasedCompensationExpense",
    ],
    "deferred_income_taxes": [
        "DeferredIncomeTaxExpenseBenefit",
    ],
    "change_in_receivables": [
        "IncreaseDecreaseInAccountsReceivable",
    ],
    "change_in_inventory": [
        "IncreaseDecreaseInInventories",
    ],
    "change_in_payables": [
        "IncreaseDecreaseInAccountsPayable",
    ],
    "other_operating_activities": [
        "OtherOperatingActivitiesCashFlowStatement",
    ],
    "net_cash_from_operating": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],
    # Investing Activities
    "capital_expenditures": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
    "acquisitions": [
        "PaymentsToAcquireBusinessesNetOfCashAcquired",
    ],
    "purchases_of_investments": [
        "PaymentsToAcquireInvestments",
        "PaymentsToAcquireAvailableForSaleSecuritiesDebt",
    ],
    "sales_of_investments": [
        "ProceedsFromSaleOfAvailableForSaleSecuritiesDebt",
        "ProceedsFromSaleAndMaturityOfMarketableSecurities",
    ],
    "net_cash_from_investing": [
        "NetCashProvidedByUsedInInvestingActivities",
    ],
    # Financing Activities
    "debt_repayment": [
        "RepaymentsOfLongTermDebt",
        "RepaymentsOfDebt",
    ],
    "debt_issuance": [
        "ProceedsFromIssuanceOfLongTermDebt",
        "ProceedsFromDebtNetOfIssuanceCosts",
    ],
    "share_repurchases": [
        "PaymentsForRepurchaseOfCommonStock",
    ],
    "dividends_paid": [
        "PaymentsOfDividendsCommonStock",
        "PaymentsOfDividends",
    ],
    "stock_issuance": [
        "ProceedsFromIssuanceOfCommonStock",
        "ProceedsFromStockOptionsExercised",
    ],
    "net_cash_from_financing": [
        "NetCashProvidedByUsedInFinancingActivities",
    ],
    # Net Change
    "effect_of_exchange_rate": [
        "EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
        "EffectOfExchangeRateOnCashAndCashEquivalents",
    ],
    "net_change_in_cash": [
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
        "CashAndCashEquivalentsPeriodIncreaseDecrease",
    ],
}

# Segment-related XBRL axes
SEGMENT_AXES = {
    "business": [
        "StatementBusinessSegmentsAxis",
        "SegmentReportingInformationBySegmentAxis",
    ],
    "geographic": [
        "StatementGeographicalAxis",
    ],
    "product": [
        "ProductOrServiceAxis",
    ],
}

# Segment metrics
SEGMENT_METRICS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
    ],
    "operating_income": [
        "OperatingIncomeLoss",
        "GrossProfit",
    ],
    "assets": [
        "Assets",
        "NoncurrentAssets",
    ],
}

# Items that should be negated for display (expenses shown as positive)
NEGATED_ITEMS = {
    "cost_of_revenue",
    "research_and_development",
    "selling_general_admin",
    "operating_expenses",
    "interest_expense",
    "income_tax_expense",
    "capital_expenditures",
    "acquisitions",
    "purchases_of_investments",
    "debt_repayment",
    "share_repurchases",
    "dividends_paid",
    "treasury_stock",
}

# Human-readable labels for line items
LABELS = {
    # Income Statement
    "revenue": "Revenue",
    "cost_of_revenue": "Cost of Revenue",
    "gross_profit": "Gross Profit",
    "research_and_development": "Research & Development",
    "selling_general_admin": "Selling, General & Administrative",
    "operating_expenses": "Operating Expenses",
    "operating_income": "Operating Income",
    "interest_expense": "Interest Expense",
    "interest_income": "Interest Income",
    "other_income_expense": "Other Income (Expense)",
    "income_before_tax": "Income Before Tax",
    "income_tax_expense": "Income Tax Expense",
    "net_income": "Net Income",
    "eps_basic": "EPS (Basic)",
    "eps_diluted": "EPS (Diluted)",
    "shares_basic": "Shares Outstanding (Basic)",
    "shares_diluted": "Shares Outstanding (Diluted)",
    # Balance Sheet
    "cash_and_equivalents": "Cash & Cash Equivalents",
    "short_term_investments": "Short-Term Investments",
    "accounts_receivable": "Accounts Receivable",
    "inventory": "Inventory",
    "prepaid_expenses": "Prepaid Expenses",
    "total_current_assets": "Total Current Assets",
    "property_plant_equipment": "Property, Plant & Equipment",
    "goodwill": "Goodwill",
    "intangible_assets": "Intangible Assets",
    "long_term_investments": "Long-Term Investments",
    "other_assets": "Other Assets",
    "total_assets": "Total Assets",
    "accounts_payable": "Accounts Payable",
    "accrued_liabilities": "Accrued Liabilities",
    "deferred_revenue_current": "Deferred Revenue (Current)",
    "short_term_debt": "Short-Term Debt",
    "current_portion_long_term_debt": "Current Portion of Long-Term Debt",
    "total_current_liabilities": "Total Current Liabilities",
    "long_term_debt": "Long-Term Debt",
    "deferred_tax_liabilities": "Deferred Tax Liabilities",
    "other_liabilities": "Other Liabilities",
    "total_liabilities": "Total Liabilities",
    "common_stock": "Common Stock",
    "additional_paid_in_capital": "Additional Paid-In Capital",
    "retained_earnings": "Retained Earnings",
    "accumulated_other_comprehensive_income": "Accumulated Other Comprehensive Income",
    "treasury_stock": "Treasury Stock",
    "total_stockholders_equity": "Total Stockholders' Equity",
    "total_liabilities_and_equity": "Total Liabilities & Equity",
    # Cash Flow
    "net_income_cf": "Net Income",
    "depreciation_amortization": "Depreciation & Amortization",
    "stock_based_compensation": "Stock-Based Compensation",
    "deferred_income_taxes": "Deferred Income Taxes",
    "change_in_receivables": "Change in Receivables",
    "change_in_inventory": "Change in Inventory",
    "change_in_payables": "Change in Payables",
    "other_operating_activities": "Other Operating Activities",
    "net_cash_from_operating": "Net Cash from Operating Activities",
    "capital_expenditures": "Capital Expenditures",
    "acquisitions": "Acquisitions",
    "purchases_of_investments": "Purchases of Investments",
    "sales_of_investments": "Sales of Investments",
    "net_cash_from_investing": "Net Cash from Investing Activities",
    "debt_repayment": "Debt Repayment",
    "debt_issuance": "Debt Issuance",
    "share_repurchases": "Share Repurchases",
    "dividends_paid": "Dividends Paid",
    "stock_issuance": "Stock Issuance",
    "net_cash_from_financing": "Net Cash from Financing Activities",
    "effect_of_exchange_rate": "Effect of Exchange Rate",
    "net_change_in_cash": "Net Change in Cash",
}
