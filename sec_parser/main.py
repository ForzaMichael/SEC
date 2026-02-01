"""Main entry point for SEC filing parser."""

import argparse
import logging
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from .client import SECClient
from .excel_exporter import ExcelExporter
from .extractor import FinancialExtractor, extract_metadata
from .models import ParsedFiling

logger = logging.getLogger(__name__)


def parse_sec_filing(
    ticker: str,
    form_type: str = "10-K",
    year: Optional[int] = None,
    output_dir: Optional[str] = None,
) -> str:
    """
    Parse SEC filing and export to Excel.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        form_type: Filing type - "10-K" for annual, "10-Q" for quarterly
        year: Fiscal year (default: most recent filing)
        output_dir: Output directory (default: current directory)

    Returns:
        Path to the generated Excel file

    Raises:
        ValueError: If ticker is invalid or no filings found
    """
    # Initialize SEC client
    client = SECClient()

    # Look up CIK for ticker
    logger.info(f"Looking up company: {ticker}")
    cik = client.get_cik_for_ticker(ticker)
    if not cik:
        raise ValueError(f"Could not find CIK for ticker '{ticker}'")

    logger.info(f"Found CIK: {cik}")

    # Get filings list
    logger.info(f"Fetching {form_type} filings...")
    filings = client.get_filings(cik, form_type=form_type)
    if not filings:
        raise ValueError(f"No {form_type} filings found for {ticker}")

    # Select filing by year or get most recent
    filing_info = None
    if year:
        for f in filings:
            report_date = f.get('report_date', '')
            if report_date:
                filing_year = int(report_date[:4])
                if filing_year == year:
                    filing_info = f
                    break
        if not filing_info:
            raise ValueError(f"No {form_type} filing found for year {year}")
    else:
        filing_info = filings[0]

    logger.info(f"Processing filing: {filing_info.get('accession_number', 'unknown')}")

    # Get XBRL facts
    logger.info("Fetching XBRL data...")
    xbrl_facts = client.get_xbrl_facts(cik)
    if not xbrl_facts:
        raise ValueError("Could not fetch XBRL data for this company")

    # Extract metadata
    metadata = extract_metadata(filing_info, xbrl_facts)
    logger.info(f"Company: {metadata.company_name}")
    logger.info(f"Period: {metadata.period_end}")

    # Determine period dates
    period_end = metadata.period_end
    if form_type == "10-K":
        # Annual report - typically 12 months
        # Calculate start as one year prior + 1 day
        try:
            period_start = date(period_end.year - 1, period_end.month, period_end.day) + timedelta(days=1)
        except ValueError:
            # Handle leap year edge case (Feb 29)
            period_start = date(period_end.year - 1, period_end.month, 1) + timedelta(days=period_end.day)
    else:
        # Quarterly report - 3 months
        period_start = period_end - timedelta(days=90)

    fiscal_year = period_end.year
    fiscal_period = "FY" if form_type == "10-K" else metadata.fiscal_period

    # Extract financial data
    logger.info("Extracting financial statements...")
    extractor = FinancialExtractor(xbrl_facts, filing_info)

    income_statement = extractor.extract_income_statement(
        period_end, period_start, fiscal_year, fiscal_period, form_type
    )
    logger.info(f"  Income Statement: {len(income_statement.line_items)} items")

    balance_sheet = extractor.extract_balance_sheet(
        period_end, fiscal_year, fiscal_period, form_type
    )
    logger.info(f"  Balance Sheet: {len(balance_sheet.line_items)} items")

    cash_flow = extractor.extract_cash_flow(
        period_end, period_start, fiscal_year, fiscal_period, form_type
    )
    logger.info(f"  Cash Flow: {len(cash_flow.line_items)} items")

    segment_data = extractor.extract_segments(
        period_end, period_start, fiscal_year, fiscal_period
    )
    logger.info(
        f"  Segments: {len(segment_data.business_segments)} business, "
        f"{len(segment_data.geographic_segments)} geographic"
    )

    # Create parsed filing object
    parsed = ParsedFiling(
        metadata=metadata,
        income_statement=income_statement,
        balance_sheet=balance_sheet,
        cash_flow_statement=cash_flow,
        segment_data=segment_data,
    )

    # Export to Excel
    output_dir = Path(output_dir) if output_dir else Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{ticker}_{form_type}_{fiscal_year}.xlsx"
    output_path = output_dir / filename

    logger.info(f"Exporting to Excel: {output_path}")
    exporter = ExcelExporter()
    exporter.export(parsed, str(output_path))

    logger.info("Done!")
    return str(output_path)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Parse SEC filings and extract financial statements to Excel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s AAPL                    # Parse Apple's latest 10-K
  %(prog)s MSFT --form 10-Q        # Parse Microsoft's latest 10-Q
  %(prog)s GOOGL --year 2023       # Parse Alphabet's 2023 10-K
  %(prog)s AMZN -o ./reports       # Save to specific directory
        """,
    )

    parser.add_argument(
        "ticker",
        help="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)",
    )
    parser.add_argument(
        "--form", "-f",
        choices=["10-K", "10-Q"],
        default="10-K",
        help="Filing type (default: 10-K)",
    )
    parser.add_argument(
        "--year", "-y",
        type=int,
        help="Fiscal year (default: most recent)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
    )

    try:
        output_path = parse_sec_filing(
            ticker=args.ticker.upper(),
            form_type=args.form,
            year=args.year,
            output_dir=args.output,
        )
        print(f"\nSaved to: {output_path}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
