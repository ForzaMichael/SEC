"""SEC EDGAR API client for fetching filings."""

import logging
import time
from datetime import date
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

import requests

logger = logging.getLogger(__name__)

# SEC EDGAR base URLs
SEC_BASE_URL = "https://www.sec.gov"
SEC_DATA_URL = "https://data.sec.gov"

# SEC requires a User-Agent header
DEFAULT_USER_AGENT = "SEC Filing Parser/1.0 (Contact: user@example.com)"

# Rate limiting: SEC allows 10 requests per second
REQUEST_DELAY = 0.1


class SECClient:
    """Client for SEC EDGAR API."""

    def __init__(self, user_agent: str = DEFAULT_USER_AGENT):
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept-Encoding": "gzip, deflate",
        })
        self._last_request_time = 0

    def _rate_limit(self) -> None:
        """Enforce SEC rate limiting."""
        elapsed = time.time() - self._last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

    def _get(self, url: str) -> requests.Response:
        """Make a rate-limited GET request."""
        self._rate_limit()
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def get_cik_for_ticker(self, ticker: str) -> Optional[str]:
        """Look up CIK for a ticker symbol."""
        url = f"{SEC_BASE_URL}/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K&dateb=&owner=include&count=1&output=atom"
        try:
            response = self._get(url)
            # Parse the Atom feed to extract CIK
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            # Look for company-info
            for entry in root.findall('.//atom:entry', ns):
                cik_elem = entry.find('.//atom:cik', {'atom': 'http://www.w3.org/2005/Atom'})
                if cik_elem is not None:
                    return cik_elem.text.zfill(10)

            # Alternative: try the company tickers JSON
            return self._get_cik_from_tickers_json(ticker)
        except Exception as e:
            logger.warning(f"Error looking up CIK for {ticker}: {e}")
            return self._get_cik_from_tickers_json(ticker)

    def _get_cik_from_tickers_json(self, ticker: str) -> Optional[str]:
        """Get CIK from SEC company tickers JSON."""
        url = f"{SEC_BASE_URL}/files/company_tickers.json"
        try:
            response = self._get(url)
            data = response.json()
            ticker_upper = ticker.upper()
            for entry in data.values():
                if entry.get('ticker', '').upper() == ticker_upper:
                    return str(entry['cik_str']).zfill(10)
        except Exception as e:
            logger.warning(f"Error fetching company tickers: {e}")
        return None

    def get_company_info(self, cik: str) -> Dict[str, Any]:
        """Get company information from SEC."""
        cik_padded = cik.zfill(10)
        url = f"{SEC_DATA_URL}/submissions/CIK{cik_padded}.json"
        response = self._get(url)
        return response.json()

    def get_filings(
        self,
        cik: str,
        form_type: str = "10-K",
        count: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get list of filings for a company."""
        company_info = self.get_company_info(cik)

        filings = []
        recent = company_info.get('filings', {}).get('recent', {})

        forms = recent.get('form', [])
        accession_numbers = recent.get('accessionNumber', [])
        filing_dates = recent.get('filingDate', [])
        report_dates = recent.get('reportDate', [])
        primary_docs = recent.get('primaryDocument', [])

        for i, form in enumerate(forms):
            if form == form_type:
                filings.append({
                    'form': form,
                    'accession_number': accession_numbers[i],
                    'filing_date': filing_dates[i],
                    'report_date': report_dates[i],
                    'primary_document': primary_docs[i],
                    'cik': cik,
                    'company_name': company_info.get('name', ''),
                    'ticker': company_info.get('tickers', [None])[0],
                })
                if len(filings) >= count:
                    break

        return filings

    def get_filing_documents(self, cik: str, accession_number: str) -> List[Dict[str, Any]]:
        """Get list of documents in a filing."""
        cik_padded = cik.zfill(10)
        accession_clean = accession_number.replace('-', '')
        url = f"{SEC_DATA_URL}/submissions/CIK{cik_padded}.json"

        # Get the filing index
        index_url = f"{SEC_BASE_URL}/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40&output=atom"

        # For now, construct document URLs directly
        base_url = f"{SEC_BASE_URL}/Archives/edgar/data/{cik_padded}/{accession_clean}"

        return [{
            'base_url': base_url,
            'accession_number': accession_number,
        }]

    def get_xbrl_facts(self, cik: str) -> Dict[str, Any]:
        """Get XBRL company facts from SEC."""
        cik_padded = cik.zfill(10)
        url = f"{SEC_DATA_URL}/api/xbrl/companyfacts/CIK{cik_padded}.json"
        response = self._get(url)
        return response.json()

    def get_filing_xbrl(self, cik: str, accession_number: str) -> Optional[Dict[str, Any]]:
        """Get XBRL data for a specific filing."""
        # The company facts API provides all facts, we filter by filing
        try:
            facts = self.get_xbrl_facts(cik)
            return facts
        except Exception as e:
            logger.warning(f"Error fetching XBRL facts: {e}")
            return None
