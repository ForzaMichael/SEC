"""Financial data extraction from SEC XBRL filings."""

import logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from .mappings import (
    BALANCE_SHEET_TAGS,
    CASH_FLOW_TAGS,
    INCOME_STATEMENT_TAGS,
    LABELS,
    NEGATED_ITEMS,
    SEGMENT_AXES,
    SEGMENT_METRICS,
)
from .models import (
    FinancialStatement,
    FilingMetadata,
    LineItem,
    ParsedFiling,
    Segment,
    SegmentData,
    StatementType,
)

logger = logging.getLogger(__name__)


class FinancialExtractor:
    """Extracts financial data from SEC XBRL company facts."""

    def __init__(self, xbrl_facts: Dict[str, Any], filing_info: Dict[str, Any]):
        """
        Initialize extractor with XBRL facts.

        Args:
            xbrl_facts: Company facts from SEC XBRL API
            filing_info: Filing metadata dict
        """
        self.xbrl_facts = xbrl_facts
        self.filing_info = filing_info
        self.facts_by_concept: Dict[str, List[Dict]] = {}
        self._index_facts()

    def _index_facts(self) -> None:
        """Index all XBRL facts by concept name for fast lookup."""
        facts_data = self.xbrl_facts.get('facts', {})

        # Process us-gaap namespace
        us_gaap = facts_data.get('us-gaap', {})
        for concept, concept_data in us_gaap.items():
            units = concept_data.get('units', {})
            for unit_type, values in units.items():
                if concept not in self.facts_by_concept:
                    self.facts_by_concept[concept] = []
                for val in values:
                    self.facts_by_concept[concept].append({
                        'value': val.get('val'),
                        'end': val.get('end'),
                        'start': val.get('start'),
                        'fy': val.get('fy'),
                        'fp': val.get('fp'),
                        'form': val.get('form'),
                        'filed': val.get('filed'),
                        'accn': val.get('accn'),
                        'frame': val.get('frame'),
                        'unit': unit_type,
                    })

        # Process dei namespace (for shares, etc.)
        dei = facts_data.get('dei', {})
        for concept, concept_data in dei.items():
            units = concept_data.get('units', {})
            for unit_type, values in units.items():
                if concept not in self.facts_by_concept:
                    self.facts_by_concept[concept] = []
                for val in values:
                    self.facts_by_concept[concept].append({
                        'value': val.get('val'),
                        'end': val.get('end'),
                        'start': val.get('start'),
                        'fy': val.get('fy'),
                        'fp': val.get('fp'),
                        'form': val.get('form'),
                        'filed': val.get('filed'),
                        'accn': val.get('accn'),
                        'frame': val.get('frame'),
                        'unit': unit_type,
                    })

    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str[:10], '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None

    def _find_fact_value(
        self,
        tag_candidates: List[str],
        period_end: date,
        period_start: Optional[date] = None,
        fiscal_year: Optional[int] = None,
        fiscal_period: Optional[str] = None,
        form_type: Optional[str] = None,
        tolerance_days: int = 5,
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Find a fact value matching the given criteria.

        Args:
            tag_candidates: List of concept names to try (in priority order)
            period_end: Target period end date
            period_start: Target period start date (None for instant/balance sheet)
            fiscal_year: Target fiscal year
            fiscal_period: Target fiscal period (FY, Q1, Q2, Q3, Q4)
            form_type: Target form type (10-K, 10-Q)
            tolerance_days: Date matching tolerance

        Returns:
            Tuple of (value, matched_tag) or (None, None) if not found
        """
        for tag in tag_candidates:
            if tag not in self.facts_by_concept:
                continue

            # Sort facts by end date descending to get most recent first
            sorted_facts = sorted(
                self.facts_by_concept[tag],
                key=lambda x: x.get('end', '') or '',
                reverse=True
            )

            for fact in sorted_facts:
                # Check form type if specified
                if form_type and fact.get('form') != form_type:
                    continue

                # Check period end date
                fact_end = self._parse_date(fact.get('end'))
                if not fact_end:
                    continue

                end_delta = abs((fact_end - period_end).days)
                if end_delta > tolerance_days:
                    continue

                # For duration facts, check start date if available
                if period_start:
                    fact_start = self._parse_date(fact.get('start'))
                    if fact_start:
                        start_delta = abs((fact_start - period_start).days)
                        if start_delta > tolerance_days:
                            continue

                # Return the value
                try:
                    value = fact['value']
                    if value is not None:
                        return float(value), tag
                except (ValueError, TypeError):
                    continue

        return None, None

    def extract_income_statement(
        self,
        period_end: date,
        period_start: date,
        fiscal_year: int,
        fiscal_period: str,
        form_type: str = "10-K",
    ) -> FinancialStatement:
        """Extract income statement for the specified period."""
        statement = FinancialStatement(
            statement_type=StatementType.INCOME_STATEMENT,
            period_end=period_end,
            period_start=period_start,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
        )

        for key, tag_candidates in INCOME_STATEMENT_TAGS.items():
            value, matched_tag = self._find_fact_value(
                tag_candidates,
                period_end,
                period_start,
                fiscal_year=fiscal_year,
                fiscal_period=fiscal_period,
                form_type=form_type,
            )

            if value is not None:
                statement.add_line_item(
                    key,
                    LineItem(
                        label=LABELS.get(key, key),
                        xbrl_tag=matched_tag or "",
                        value=value,
                        period_start=period_start,
                        period_end=period_end,
                        is_negated=key in NEGATED_ITEMS,
                    ),
                )

        return statement

    def extract_balance_sheet(
        self,
        period_end: date,
        fiscal_year: int,
        fiscal_period: str,
        form_type: str = "10-K",
    ) -> FinancialStatement:
        """Extract balance sheet for the specified date (instant)."""
        statement = FinancialStatement(
            statement_type=StatementType.BALANCE_SHEET,
            period_end=period_end,
            period_start=None,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
        )

        for key, tag_candidates in BALANCE_SHEET_TAGS.items():
            value, matched_tag = self._find_fact_value(
                tag_candidates,
                period_end,
                period_start=None,
                fiscal_year=fiscal_year,
                fiscal_period=fiscal_period,
                form_type=form_type,
            )

            if value is not None:
                statement.add_line_item(
                    key,
                    LineItem(
                        label=LABELS.get(key, key),
                        xbrl_tag=matched_tag or "",
                        value=value,
                        period_end=period_end,
                        is_negated=key in NEGATED_ITEMS,
                    ),
                )

        return statement

    def extract_cash_flow(
        self,
        period_end: date,
        period_start: date,
        fiscal_year: int,
        fiscal_period: str,
        form_type: str = "10-K",
    ) -> FinancialStatement:
        """Extract cash flow statement for the specified period."""
        statement = FinancialStatement(
            statement_type=StatementType.CASH_FLOW,
            period_end=period_end,
            period_start=period_start,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
        )

        for key, tag_candidates in CASH_FLOW_TAGS.items():
            value, matched_tag = self._find_fact_value(
                tag_candidates,
                period_end,
                period_start,
                fiscal_year=fiscal_year,
                fiscal_period=fiscal_period,
                form_type=form_type,
            )

            if value is not None:
                statement.add_line_item(
                    key,
                    LineItem(
                        label=LABELS.get(key, key),
                        xbrl_tag=matched_tag or "",
                        value=value,
                        period_start=period_start,
                        period_end=period_end,
                        is_negated=key in NEGATED_ITEMS,
                    ),
                )

        return statement

    def extract_segments(
        self,
        period_end: date,
        period_start: date,
        fiscal_year: int,
        fiscal_period: str,
    ) -> SegmentData:
        """
        Extract segment performance data.

        Note: Segment data in the company facts API is limited.
        Full segment extraction requires parsing the XBRL instance document.
        """
        segment_data = SegmentData(
            period_end=period_end,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
        )

        # The SEC company facts API doesn't include dimensional data
        # For full segment data, we would need to parse the XBRL instance
        # This is a simplified implementation

        return segment_data


def extract_metadata(filing_info: Dict[str, Any], xbrl_facts: Dict[str, Any]) -> FilingMetadata:
    """Extract metadata from filing info and XBRL facts."""
    report_date = filing_info.get('report_date', '')
    if isinstance(report_date, str) and report_date:
        period_end = datetime.strptime(report_date[:10], '%Y-%m-%d').date()
    else:
        period_end = date.today()

    filing_date = filing_info.get('filing_date', '')
    if isinstance(filing_date, str) and filing_date:
        filing_date = datetime.strptime(filing_date[:10], '%Y-%m-%d').date()
    else:
        filing_date = date.today()

    form_type = filing_info.get('form', '10-K')
    fiscal_year = period_end.year
    fiscal_period = "FY" if "10-K" in str(form_type) else "Q"

    return FilingMetadata(
        cik=str(filing_info.get('cik', '')).zfill(10),
        company_name=xbrl_facts.get('entityName', '') or filing_info.get('company_name', ''),
        ticker=filing_info.get('ticker'),
        form_type=str(form_type),
        filing_date=filing_date,
        period_end=period_end,
        fiscal_year=fiscal_year,
        fiscal_period=fiscal_period,
        accession_number=filing_info.get('accession_number', ''),
    )
