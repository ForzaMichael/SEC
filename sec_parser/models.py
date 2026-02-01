"""Data models for SEC filing financial data."""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List, Optional


class StatementType(Enum):
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"


@dataclass
class LineItem:
    """Represents a single line item from a financial statement."""
    label: str
    xbrl_tag: str
    value: Optional[float]
    period_end: date
    period_start: Optional[date] = None
    decimals: int = -6
    is_negated: bool = False

    @property
    def display_value(self) -> Optional[float]:
        """Return value adjusted for negation (expenses shown as positive)."""
        if self.value is None:
            return None
        return -self.value if self.is_negated else self.value


@dataclass
class FinancialStatement:
    """Represents a complete financial statement."""
    statement_type: StatementType
    period_end: date
    fiscal_year: int
    fiscal_period: str
    period_start: Optional[date] = None
    line_items: Dict[str, LineItem] = field(default_factory=dict)

    def add_line_item(self, key: str, item: LineItem) -> None:
        self.line_items[key] = item

    def get_value(self, key: str) -> Optional[float]:
        item = self.line_items.get(key)
        return item.value if item else None

    def to_dict(self) -> Dict[str, Optional[float]]:
        return {key: item.display_value for key, item in self.line_items.items()}


@dataclass
class Segment:
    """Represents a business or geographic segment."""
    name: str
    segment_type: str  # "business" or "geographic"
    revenue: Optional[float] = None
    operating_income: Optional[float] = None
    assets: Optional[float] = None


@dataclass
class SegmentData:
    """Collection of segment information for a filing."""
    period_end: date
    fiscal_year: int
    fiscal_period: str
    business_segments: List[Segment] = field(default_factory=list)
    geographic_segments: List[Segment] = field(default_factory=list)


@dataclass
class FilingMetadata:
    """Metadata about the SEC filing."""
    cik: str
    company_name: str
    ticker: Optional[str]
    form_type: str
    filing_date: date
    period_end: date
    fiscal_year: int
    fiscal_period: str
    accession_number: str


@dataclass
class ParsedFiling:
    """Complete parsed SEC filing with all extracted data."""
    metadata: FilingMetadata
    income_statement: Optional[FinancialStatement] = None
    balance_sheet: Optional[FinancialStatement] = None
    cash_flow_statement: Optional[FinancialStatement] = None
    segment_data: Optional[SegmentData] = None
