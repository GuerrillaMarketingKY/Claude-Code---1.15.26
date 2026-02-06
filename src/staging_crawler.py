#!/usr/bin/env python3
"""
Staging Site Crawler - Crawls a staging domain and reports all errors.

Detects:
  - HTTP errors (4xx, 5xx status codes)
  - Broken internal and external links
  - Missing resources (images, CSS, JS, fonts)
  - Redirect chains (3+ hops)
  - SSL/TLS errors
  - Timeouts and connection failures
  - Mixed content (HTTP resources on HTTPS pages)
  - Empty pages (zero-length responses)

Usage:
  python src/staging_crawler.py <staging-url> [options]

Examples:
  python src/staging_crawler.py https://staging.example.com
  python src/staging_crawler.py https://staging.example.com --max-pages 200
  python src/staging_crawler.py https://staging.example.com --timeout 15 --output report.json
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CrawlError:
    """Represents a single error found during crawling."""
    url: str
    error_type: str
    message: str
    status_code: Optional[int] = None
    source_page: Optional[str] = None
    element: Optional[str] = None


@dataclass
class PageResult:
    """Result of crawling a single page."""
    url: str
    status_code: int
    content_type: str = ""
    content_length: int = 0
    redirect_chain: list = field(default_factory=list)
    load_time_ms: int = 0
    errors: list = field(default_factory=list)


@dataclass
class CrawlReport:
    """Full report for a crawl session."""
    base_url: str
    pages_crawled: int = 0
    total_errors: int = 0
    errors_by_type: dict = field(default_factory=dict)
    page_results: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    duration_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Crawler
# ---------------------------------------------------------------------------

class StagingCrawler:
    """Crawls a staging website and collects errors."""

    def __init__(self, base_url, max_pages=100, timeout=10, verify_ssl=True,
                 check_external=False, user_agent=None):
        parsed = urlparse(base_url)
        # Normalize: ensure scheme, strip trailing slash
        if not parsed.scheme:
            base_url = "https://" + base_url
            parsed = urlparse(base_url)
        self.base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))
        self.domain = parsed.netloc
        self.scheme = parsed.scheme
        self.max_pages = max_pages
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.check_external = check_external

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or "StagingCrawler/1.0 (error-checker)"
        })
        # Don't follow redirects automatically so we can inspect chains
        self.session.max_redirects = 10

        self.visited = set()
        self.queued = set()
        self.errors: list[CrawlError] = []
        self.page_results: list[PageResult] = []

    # -- public API ----------------------------------------------------------

    def crawl(self) -> CrawlReport:
        """Run the crawl and return a report."""
        start = time.time()
        self._enqueue(self.base_url)
        queue = [self.base_url]

        while queue and len(self.visited) < self.max_pages:
            url = queue.pop(0)
            if url in self.visited:
                continue

            new_urls = self._process_page(url)
            for u in new_urls:
                if u not in self.visited and u not in self.queued:
                    self._enqueue(u)
                    queue.append(u)

        duration = time.time() - start
        return self._build_report(duration)

    # -- internal ------------------------------------------------------------

    def _enqueue(self, url):
        self.queued.add(url)

    def _is_internal(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ""

    def _normalize(self, url, source_url):
        """Resolve relative URLs and strip fragments."""
        full = urljoin(source_url, url)
        parsed = urlparse(full)
        # Strip fragment
        normalized = urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                                  parsed.params, parsed.query, ""))
        return normalized

    def _process_page(self, url):
        """Fetch a page, record errors, extract links. Returns new URLs."""
        self.visited.add(url)
        discovered = []

        start_time = time.time()
        try:
            resp = self.session.get(url, timeout=self.timeout,
                                    verify=self.verify_ssl, allow_redirects=True)
        except requests.exceptions.SSLError as exc:
            self._add_error(url, "ssl_error", f"SSL/TLS error: {exc}")
            self._print_error(url, "SSL_ERROR", str(exc))
            return discovered
        except requests.exceptions.ConnectionError as exc:
            self._add_error(url, "connection_error", f"Connection failed: {exc}")
            self._print_error(url, "CONN_ERROR", str(exc))
            return discovered
        except requests.exceptions.Timeout:
            self._add_error(url, "timeout", f"Request timed out after {self.timeout}s")
            self._print_error(url, "TIMEOUT", f">{self.timeout}s")
            return discovered
        except requests.exceptions.RequestException as exc:
            self._add_error(url, "request_error", f"Request error: {exc}")
            self._print_error(url, "REQ_ERROR", str(exc))
            return discovered

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Build redirect chain
        redirect_chain = [r.url for r in resp.history] if resp.history else []

        content_type = resp.headers.get("Content-Type", "")
        result = PageResult(
            url=url,
            status_code=resp.status_code,
            content_type=content_type,
            content_length=len(resp.content),
            redirect_chain=redirect_chain,
            load_time_ms=elapsed_ms,
        )
        self.page_results.append(result)

        # Log progress
        status_indicator = "OK" if 200 <= resp.status_code < 300 else f"ERR {resp.status_code}"
        print(f"  [{status_indicator}] {url} ({elapsed_ms}ms)")

        # --- Error checks ---

        # 1. HTTP error status codes
        if resp.status_code >= 400:
            error_type = "client_error" if resp.status_code < 500 else "server_error"
            self._add_error(url, error_type,
                            f"HTTP {resp.status_code} {resp.reason}",
                            status_code=resp.status_code)

        # 2. Long redirect chains (3+ hops)
        if len(redirect_chain) >= 3:
            chain_str = " -> ".join(redirect_chain + [resp.url])
            self._add_error(url, "redirect_chain",
                            f"Redirect chain with {len(redirect_chain)} hops: {chain_str}")

        # 3. Empty response body on success
        if 200 <= resp.status_code < 300 and len(resp.content) == 0:
            self._add_error(url, "empty_response", "Page returned empty body (0 bytes)")

        # Stop parsing if not HTML
        if "text/html" not in content_type:
            return discovered

        # Parse HTML
        try:
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            soup = BeautifulSoup(resp.text, "html.parser")

        # 4. Check all links (<a href>)
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            link_url = self._normalize(href, url)
            if self._is_internal(link_url):
                discovered.append(link_url)
            elif self.check_external:
                self._check_resource(link_url, url, "external_link")

        # 5. Check images
        for tag in soup.find_all("img", src=True):
            img_url = self._normalize(tag["src"], url)
            self._check_resource(img_url, url, "image")

        # 6. Check stylesheets
        for tag in soup.find_all("link", rel=True, href=True):
            if "stylesheet" in tag.get("rel", []):
                css_url = self._normalize(tag["href"], url)
                self._check_resource(css_url, url, "stylesheet")

        # 7. Check scripts
        for tag in soup.find_all("script", src=True):
            js_url = self._normalize(tag["src"], url)
            self._check_resource(js_url, url, "script")

        # 8. Mixed content detection (HTTP resource on HTTPS page)
        if self.scheme == "https":
            self._check_mixed_content(soup, url)

        return discovered

    def _check_resource(self, resource_url, source_page, resource_type):
        """HEAD-check a resource URL and record errors."""
        # Skip data URIs
        if resource_url.startswith("data:"):
            return
        # Skip already-checked URLs to avoid duplicate work
        cache_key = resource_url
        if cache_key in self.visited:
            return
        # Don't add to main visited set (we still want to crawl pages)
        # but track checked resources separately
        if not hasattr(self, "_checked_resources"):
            self._checked_resources = set()
        if cache_key in self._checked_resources:
            return
        self._checked_resources.add(cache_key)

        try:
            resp = self.session.head(resource_url, timeout=self.timeout,
                                     verify=self.verify_ssl, allow_redirects=True)
            if resp.status_code >= 400:
                self._add_error(
                    resource_url,
                    f"broken_{resource_type}",
                    f"Broken {resource_type}: HTTP {resp.status_code}",
                    status_code=resp.status_code,
                    source_page=source_page,
                    element=resource_type,
                )
                self._print_error(resource_url, f"BROKEN_{resource_type.upper()}", f"HTTP {resp.status_code}", source_page)
        except requests.exceptions.SSLError:
            self._add_error(resource_url, f"broken_{resource_type}",
                            f"SSL error loading {resource_type}",
                            source_page=source_page, element=resource_type)
        except requests.exceptions.ConnectionError:
            self._add_error(resource_url, f"broken_{resource_type}",
                            f"Connection failed for {resource_type}",
                            source_page=source_page, element=resource_type)
        except requests.exceptions.Timeout:
            self._add_error(resource_url, f"broken_{resource_type}",
                            f"Timeout loading {resource_type}",
                            source_page=source_page, element=resource_type)
        except requests.exceptions.RequestException as exc:
            self._add_error(resource_url, f"broken_{resource_type}",
                            f"Error loading {resource_type}: {exc}",
                            source_page=source_page, element=resource_type)

    def _check_mixed_content(self, soup, source_url):
        """Detect HTTP resources loaded on an HTTPS page."""
        http_attrs = [
            ("img", "src"), ("script", "src"), ("link", "href"),
            ("iframe", "src"), ("video", "src"), ("audio", "src"),
            ("source", "src"), ("object", "data"),
        ]
        for tag_name, attr in http_attrs:
            for tag in soup.find_all(tag_name, **{attr: True}):
                val = tag[attr]
                if val.startswith("http://"):
                    self._add_error(
                        val, "mixed_content",
                        f"Mixed content: HTTP resource loaded on HTTPS page",
                        source_page=source_url,
                        element=f"<{tag_name} {attr}=\"{val}\">"
                    )

    def _add_error(self, url, error_type, message, status_code=None,
                   source_page=None, element=None):
        self.errors.append(CrawlError(
            url=url,
            error_type=error_type,
            message=message,
            status_code=status_code,
            source_page=source_page,
            element=element,
        ))

    def _print_error(self, url, tag, detail, source=None):
        source_info = f" (linked from {source})" if source else ""
        print(f"  ** [{tag}] {url} - {detail}{source_info}")

    def _build_report(self, duration) -> CrawlReport:
        errors_by_type = defaultdict(int)
        for e in self.errors:
            errors_by_type[e.error_type] += 1

        return CrawlReport(
            base_url=self.base_url,
            pages_crawled=len(self.visited),
            total_errors=len(self.errors),
            errors_by_type=dict(errors_by_type),
            page_results=[asdict(p) for p in self.page_results],
            errors=[asdict(e) for e in self.errors],
            duration_seconds=round(duration, 2),
        )


# ---------------------------------------------------------------------------
# CLI & display
# ---------------------------------------------------------------------------

def print_report(report: CrawlReport):
    """Print a human-readable summary of the crawl report."""
    print("\n" + "=" * 70)
    print("  STAGING SITE CRAWL REPORT")
    print("=" * 70)
    print(f"  Base URL:       {report.base_url}")
    print(f"  Pages crawled:  {report.pages_crawled}")
    print(f"  Total errors:   {report.total_errors}")
    print(f"  Duration:       {report.duration_seconds}s")
    print("-" * 70)

    if not report.errors:
        print("\n  No errors found! The staging site looks clean.\n")
        return

    # Summary by type
    print("\n  ERRORS BY TYPE:")
    for error_type, count in sorted(report.errors_by_type.items(),
                                     key=lambda x: -x[1]):
        label = error_type.replace("_", " ").title()
        print(f"    {label:<30} {count}")

    # Detailed error list
    print(f"\n  DETAILED ERRORS ({report.total_errors}):")
    print("-" * 70)
    for i, err in enumerate(report.errors, 1):
        print(f"\n  [{i}] {err['error_type'].replace('_', ' ').upper()}")
        print(f"      URL:     {err['url']}")
        print(f"      Detail:  {err['message']}")
        if err.get("status_code"):
            print(f"      Status:  {err['status_code']}")
        if err.get("source_page"):
            print(f"      Source:  {err['source_page']}")
        if err.get("element"):
            print(f"      Element: {err['element']}")

    # Pages with errors
    error_pages = [p for p in report.page_results if p.get("errors") or
                   (p.get("status_code") and p["status_code"] >= 400)]
    if error_pages:
        print(f"\n  PAGES WITH HTTP ERRORS:")
        print("-" * 70)
        for p in error_pages:
            print(f"    [{p['status_code']}] {p['url']}")

    print("\n" + "=" * 70)


def save_report(report: CrawlReport, output_path: str):
    """Save the full report as JSON."""
    with open(output_path, "w") as f:
        json.dump(asdict(report), f, indent=2)
    print(f"\n  Full report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Crawl a staging website and find all errors.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://staging.example.com
  %(prog)s https://staging.example.com --max-pages 200 --timeout 15
  %(prog)s https://staging.example.com --check-external --output report.json
  %(prog)s https://staging.example.com --no-verify-ssl
        """
    )
    parser.add_argument("url", help="The staging site URL to crawl")
    parser.add_argument("--max-pages", type=int, default=100,
                        help="Maximum number of pages to crawl (default: 100)")
    parser.add_argument("--timeout", type=int, default=10,
                        help="Request timeout in seconds (default: 10)")
    parser.add_argument("--no-verify-ssl", action="store_true",
                        help="Disable SSL certificate verification")
    parser.add_argument("--check-external", action="store_true",
                        help="Also check external links (slower)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Save full JSON report to this file path")
    parser.add_argument("--user-agent", type=str, default=None,
                        help="Custom User-Agent string")

    args = parser.parse_args()

    print(f"\n  Starting crawl of: {args.url}")
    print(f"  Max pages: {args.max_pages} | Timeout: {args.timeout}s")
    print(f"  SSL verify: {not args.no_verify_ssl} | Check external: {args.check_external}")
    print("-" * 70)

    crawler = StagingCrawler(
        base_url=args.url,
        max_pages=args.max_pages,
        timeout=args.timeout,
        verify_ssl=not args.no_verify_ssl,
        check_external=args.check_external,
        user_agent=args.user_agent,
    )

    report = crawler.crawl()
    print_report(report)

    if args.output:
        save_report(report, args.output)

    # Exit with non-zero code if errors were found
    sys.exit(1 if report.total_errors > 0 else 0)


if __name__ == "__main__":
    main()
