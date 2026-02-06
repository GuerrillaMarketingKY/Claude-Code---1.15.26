#!/usr/bin/env python3
"""
Staging Site QA Report Generator for Web Designers

Crawls a staging website and produces a detailed bullet-point report
for every page found, flagging:
  - HTTP errors (404, 500, etc.)
  - Broken internal and external links
  - Broken/missing images
  - Broken stylesheets and scripts
  - Blank/stub pages (only header + footer, no real content)
  - Pages with very little content (thin pages)
  - Missing page titles or meta descriptions
  - Missing alt text on images
  - Mixed content warnings (HTTP on HTTPS)
  - Redirect chains
  - Placeholder/lorem ipsum text
  - Missing Open Graph tags
  - Large images (potential performance issues)
  - Forms with no action or broken action URLs
  - Empty links (anchors with no text)

Usage:
  python src/staging_qa_report.py https://staging.example.com
  python src/staging_qa_report.py https://staging.example.com --wp-user admin --wp-pass secret
  python src/staging_qa_report.py https://staging.example.com --max-pages 300 -o qa_report.md
"""

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup, Comment


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PageIssue:
    severity: str  # "critical", "warning", "info"
    category: str  # "broken_link", "design", "seo", "performance", etc.
    message: str


@dataclass
class PageReport:
    url: str
    status_code: int = 0
    title: str = ""
    load_time_ms: int = 0
    content_length: int = 0
    word_count: int = 0
    issues: list = field(default_factory=list)
    links_found: int = 0
    images_found: int = 0
    is_blank: bool = False


# ---------------------------------------------------------------------------
# Crawler + Analyzer
# ---------------------------------------------------------------------------

class QAReportCrawler:

    PLACEHOLDER_PATTERNS = [
        r"lorem\s+ipsum",
        r"dolor\s+sit\s+amet",
        r"consectetur\s+adipiscing",
        r"placeholder\s+text",
        r"your\s+content\s+here",
        r"coming\s+soon",
        r"under\s+construction",
        r"page\s+not\s+found",
        r"example\.com",
        r"test\s+page",
        r"hello\s+world",
        r"sample\s+page",
        r"this\s+is\s+a\s+test",
    ]

    THIN_CONTENT_THRESHOLD = 50    # words
    BLANK_CONTENT_THRESHOLD = 20   # words (just nav + footer text)
    LARGE_IMAGE_BYTES = 500_000    # 500KB

    def __init__(self, base_url, max_pages=200, timeout=15, verify_ssl=True,
                 check_external=True, no_proxy=False):
        parsed = urlparse(base_url)
        if not parsed.scheme:
            base_url = "https://" + base_url
            parsed = urlparse(base_url)
        self.base_url = urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", "")
        )
        self.domain = parsed.netloc
        self.scheme = parsed.scheme
        self.max_pages = max_pages
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.check_external = check_external

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        })
        if no_proxy:
            self.session.trust_env = False
        self.session.max_redirects = 10

        self.visited: set[str] = set()
        self.queued: set[str] = set()
        self._checked_resources: dict[str, Optional[int]] = {}
        self.page_reports: list[PageReport] = []

    # -- WordPress login -----------------------------------------------------

    def wp_login(self, username, password):
        login_url = self.base_url + "/wp-login.php"
        print(f"  Logging in to WordPress as '{username}' ...")
        try:
            resp = self.session.post(login_url, data={
                "log": username, "pwd": password,
                "wp-submit": "Log In",
                "redirect_to": self.base_url + "/wp-admin/",
                "testcookie": "1",
            }, timeout=self.timeout, verify=self.verify_ssl, allow_redirects=True)
            if resp.status_code == 200 and "wp-admin" in resp.url:
                print(f"  Login successful.\n")
                return True
            print(f"  Login may have failed (HTTP {resp.status_code} -> {resp.url})\n")
            return False
        except requests.exceptions.RequestException as exc:
            print(f"  Login failed: {exc}\n")
            return False

    # -- Crawl ---------------------------------------------------------------

    def crawl(self) -> list[PageReport]:
        print(f"  Crawling {self.base_url} (max {self.max_pages} pages) ...\n")
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

        return self.page_reports

    # -- Internal ------------------------------------------------------------

    def _enqueue(self, url):
        self.queued.add(url)

    def _is_internal(self, url):
        return urlparse(url).netloc in (self.domain, "")

    def _normalize(self, href, source):
        full = urljoin(source, href)
        p = urlparse(full)
        return urlunparse((p.scheme, p.netloc, p.path, p.params, p.query, ""))

    def _head_check(self, url) -> Optional[int]:
        """HEAD-check a URL, return status code or None on failure."""
        if url in self._checked_resources:
            return self._checked_resources[url]
        if url.startswith("data:"):
            return 200
        try:
            r = self.session.head(url, timeout=self.timeout,
                                  verify=self.verify_ssl, allow_redirects=True)
            self._checked_resources[url] = r.status_code
            return r.status_code
        except requests.exceptions.RequestException:
            self._checked_resources[url] = None
            return None

    def _process_page(self, url):
        self.visited.add(url)
        discovered = []
        report = PageReport(url=url)

        # -- Fetch page -------------------------------------------------------
        start = time.time()
        try:
            resp = self.session.get(url, timeout=self.timeout,
                                    verify=self.verify_ssl, allow_redirects=True)
        except requests.exceptions.SSLError as exc:
            report.issues.append(PageIssue("critical", "ssl",
                                           f"SSL error: {exc}"))
            self.page_reports.append(report)
            self._log(url, "SSL_ERR")
            return discovered
        except requests.exceptions.ConnectionError as exc:
            report.issues.append(PageIssue("critical", "connection",
                                           f"Connection failed: {exc}"))
            self.page_reports.append(report)
            self._log(url, "CONN_ERR")
            return discovered
        except requests.exceptions.Timeout:
            report.issues.append(PageIssue("critical", "timeout",
                                           f"Page timed out (>{self.timeout}s)"))
            self.page_reports.append(report)
            self._log(url, "TIMEOUT")
            return discovered
        except requests.exceptions.RequestException as exc:
            report.issues.append(PageIssue("critical", "request",
                                           f"Request error: {exc}"))
            self.page_reports.append(report)
            self._log(url, "REQ_ERR")
            return discovered

        elapsed = int((time.time() - start) * 1000)
        report.status_code = resp.status_code
        report.load_time_ms = elapsed
        report.content_length = len(resp.content)
        content_type = resp.headers.get("Content-Type", "")

        self._log(url, str(resp.status_code), elapsed)

        # -- HTTP status errors ------------------------------------------------
        if resp.status_code == 404:
            report.issues.append(PageIssue("critical", "http",
                                           "404 Not Found - page does not exist"))
        elif resp.status_code == 403:
            report.issues.append(PageIssue("critical", "http",
                                           "403 Forbidden - access denied"))
        elif resp.status_code == 500:
            report.issues.append(PageIssue("critical", "http",
                                           "500 Internal Server Error"))
        elif resp.status_code >= 400:
            report.issues.append(PageIssue("critical", "http",
                                           f"HTTP {resp.status_code} {resp.reason}"))

        # -- Redirect chain ----------------------------------------------------
        if resp.history and len(resp.history) >= 3:
            chain = " -> ".join(r.url for r in resp.history) + f" -> {resp.url}"
            report.issues.append(PageIssue("warning", "redirect",
                                           f"Long redirect chain ({len(resp.history)} hops): {chain}"))

        # -- Empty body --------------------------------------------------------
        if 200 <= resp.status_code < 300 and len(resp.content) == 0:
            report.issues.append(PageIssue("critical", "design",
                                           "Completely empty response (0 bytes)"))

        # Stop if not HTML
        if "text/html" not in content_type:
            self.page_reports.append(report)
            return discovered

        # -- Parse HTML --------------------------------------------------------
        try:
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            soup = BeautifulSoup(resp.text, "html.parser")

        # -- Page title --------------------------------------------------------
        title_tag = soup.find("title")
        report.title = title_tag.get_text(strip=True) if title_tag else ""
        if not report.title:
            report.issues.append(PageIssue("warning", "seo",
                                           "Missing <title> tag"))
        elif report.title.lower() in ("untitled", "home", "page"):
            report.issues.append(PageIssue("info", "seo",
                                           f"Generic page title: \"{report.title}\""))

        # -- Meta description --------------------------------------------------
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if not meta_desc or not meta_desc.get("content", "").strip():
            report.issues.append(PageIssue("info", "seo",
                                           "Missing meta description"))

        # -- Open Graph tags ---------------------------------------------------
        og_title = soup.find("meta", property="og:title")
        og_image = soup.find("meta", property="og:image")
        if not og_title:
            report.issues.append(PageIssue("info", "seo",
                                           "Missing Open Graph og:title tag"))
        if not og_image:
            report.issues.append(PageIssue("info", "seo",
                                           "Missing Open Graph og:image tag"))

        # -- Main content analysis (blank / thin page detection) ---------------
        main_content = self._extract_main_content(soup)
        words = main_content.split()
        report.word_count = len(words)

        if len(words) <= self.BLANK_CONTENT_THRESHOLD:
            report.is_blank = True
            report.issues.append(PageIssue("critical", "design",
                                           f"BLANK PAGE - only header/footer content detected "
                                           f"({len(words)} words of actual content)"))
        elif len(words) <= self.THIN_CONTENT_THRESHOLD:
            report.issues.append(PageIssue("warning", "design",
                                           f"Very thin content - only {len(words)} words on page"))

        # -- Placeholder / lorem ipsum text ------------------------------------
        page_text = soup.get_text(" ", strip=True).lower()
        for pattern in self.PLACEHOLDER_PATTERNS:
            if re.search(pattern, page_text, re.IGNORECASE):
                report.issues.append(PageIssue("warning", "design",
                                               f"Placeholder text detected: matches \"{pattern}\""))

        # -- PHP / WordPress errors in page body -------------------------------
        php_errors = re.findall(
            r"((?:Fatal|Parse|Warning|Notice|Deprecated):\s+.{10,120})",
            resp.text
        )
        for err in php_errors[:5]:  # cap at 5
            report.issues.append(PageIssue("critical", "php_error",
                                           f"PHP error visible on page: {err.strip()}"))

        wp_db_error = re.search(r"Error establishing a database connection", resp.text)
        if wp_db_error:
            report.issues.append(PageIssue("critical", "php_error",
                                           "WordPress database connection error on page"))

        # -- Links (<a href>) --------------------------------------------------
        links = soup.find_all("a", href=True)
        report.links_found = len(links)
        broken_internal = []
        broken_external = []

        for tag in links:
            href = tag["href"]
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                # Check for empty anchors
                link_text = tag.get_text(strip=True)
                if not link_text and not tag.find("img"):
                    report.issues.append(PageIssue("warning", "design",
                                                   f"Empty link (no text/image): href=\"{href}\""))
                continue

            link_url = self._normalize(href, url)

            if self._is_internal(link_url):
                discovered.append(link_url)
                status = self._head_check(link_url)
                if status is None:
                    broken_internal.append(link_url)
                elif status >= 400:
                    broken_internal.append(f"{link_url} (HTTP {status})")
            elif self.check_external:
                status = self._head_check(link_url)
                if status is None:
                    broken_external.append(link_url)
                elif status >= 400:
                    broken_external.append(f"{link_url} (HTTP {status})")

            # Empty link text
            link_text = tag.get_text(strip=True)
            if not link_text and not tag.find("img"):
                report.issues.append(PageIssue("warning", "design",
                                               f"Empty link (no visible text): {link_url}"))

        for bl in broken_internal:
            report.issues.append(PageIssue("critical", "broken_link",
                                           f"Broken internal link: {bl}"))
        for bl in broken_external:
            report.issues.append(PageIssue("warning", "broken_link",
                                           f"Broken external link: {bl}"))

        # -- Images ------------------------------------------------------------
        images = soup.find_all("img")
        report.images_found = len(images)

        for img in images:
            src = img.get("src", "")
            alt = img.get("alt", None)

            if not src:
                report.issues.append(PageIssue("warning", "design",
                                               "Image tag with no src attribute"))
                continue

            img_url = self._normalize(src, url)

            # Missing alt text
            if alt is None or alt.strip() == "":
                short_src = src.split("/")[-1][:60] if "/" in src else src[:60]
                report.issues.append(PageIssue("warning", "accessibility",
                                               f"Missing alt text on image: {short_src}"))

            # Check if image loads
            status = self._head_check(img_url)
            if status is None:
                report.issues.append(PageIssue("critical", "broken_image",
                                               f"Broken image (connection failed): {img_url}"))
            elif status >= 400:
                report.issues.append(PageIssue("critical", "broken_image",
                                               f"Broken image (HTTP {status}): {img_url}"))

        # -- Stylesheets -------------------------------------------------------
        for tag in soup.find_all("link", rel=True, href=True):
            if "stylesheet" in tag.get("rel", []):
                css_url = self._normalize(tag["href"], url)
                status = self._head_check(css_url)
                if status is not None and status >= 400:
                    report.issues.append(PageIssue("critical", "broken_resource",
                                                   f"Broken stylesheet (HTTP {status}): {css_url}"))
                elif status is None:
                    report.issues.append(PageIssue("critical", "broken_resource",
                                                   f"Stylesheet failed to load: {css_url}"))

        # -- Scripts -----------------------------------------------------------
        for tag in soup.find_all("script", src=True):
            js_url = self._normalize(tag["src"], url)
            status = self._head_check(js_url)
            if status is not None and status >= 400:
                report.issues.append(PageIssue("critical", "broken_resource",
                                               f"Broken script (HTTP {status}): {js_url}"))
            elif status is None:
                report.issues.append(PageIssue("critical", "broken_resource",
                                               f"Script failed to load: {js_url}"))

        # -- Mixed content (HTTP resources on HTTPS page) ----------------------
        if self.scheme == "https":
            for tag_name, attr in [("img", "src"), ("script", "src"),
                                   ("link", "href"), ("iframe", "src")]:
                for tag in soup.find_all(tag_name, **{attr: True}):
                    val = tag[attr]
                    if val.startswith("http://"):
                        report.issues.append(PageIssue("warning", "mixed_content",
                                                       f"Mixed content: {val}"))

        # -- Forms with issues -------------------------------------------------
        for form in soup.find_all("form"):
            action = form.get("action", "")
            if not action:
                report.issues.append(PageIssue("info", "design",
                                               "Form with empty action attribute"))
            elif action.startswith("http://") and self.scheme == "https":
                report.issues.append(PageIssue("warning", "security",
                                               f"Form submits over HTTP (insecure): {action}"))

        # -- Slow page warning -------------------------------------------------
        if elapsed > 5000:
            report.issues.append(PageIssue("warning", "performance",
                                           f"Slow page load: {elapsed}ms"))

        self.page_reports.append(report)
        return discovered

    def _extract_main_content(self, soup):
        """Try to extract main body content, excluding header/nav/footer."""
        # Remove known non-content elements
        content_soup = BeautifulSoup(str(soup), "html.parser")
        for tag in content_soup.find_all(["header", "nav", "footer",
                                          "script", "style", "noscript"]):
            tag.decompose()
        # Also remove common WordPress header/footer classes
        for sel in [".site-header", ".site-footer", "#masthead",
                    "#colophon", ".nav-menu", ".menu-item",
                    "#site-navigation", ".widget-area", "#secondary"]:
            for el in content_soup.select(sel):
                el.decompose()
        # Remove HTML comments
        for comment in content_soup.find_all(string=lambda t: isinstance(t, Comment)):
            comment.extract()
        return content_soup.get_text(" ", strip=True)

    def _log(self, url, status, ms=0):
        ms_str = f" ({ms}ms)" if ms else ""
        print(f"  [{status}] {url}{ms_str}")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_markdown_report(reports: list[PageReport], base_url: str,
                             duration: float) -> str:
    """Generate the full Markdown QA report."""
    lines = []
    lines.append(f"# Staging Site QA Report")
    lines.append(f"**Site:** {base_url}  ")
    lines.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}  ")
    lines.append(f"**Pages crawled:** {len(reports)}  ")
    lines.append(f"**Duration:** {duration:.1f}s  ")

    # Count totals
    total_critical = sum(1 for r in reports for i in r.issues if i.severity == "critical")
    total_warnings = sum(1 for r in reports for i in r.issues if i.severity == "warning")
    total_info = sum(1 for r in reports for i in r.issues if i.severity == "info")
    blank_pages = sum(1 for r in reports if r.is_blank)
    error_pages = sum(1 for r in reports if r.status_code >= 400)
    clean_pages = sum(1 for r in reports if not r.issues)

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total pages crawled | {len(reports)} |")
    lines.append(f"| Clean pages (no issues) | {clean_pages} |")
    lines.append(f"| Pages with HTTP errors (4xx/5xx) | {error_pages} |")
    lines.append(f"| Blank/stub pages | {blank_pages} |")
    lines.append(f"| Critical issues | {total_critical} |")
    lines.append(f"| Warnings | {total_warnings} |")
    lines.append(f"| Info/minor | {total_info} |")

    # -- Issues by category summary --
    cat_counts = defaultdict(int)
    for r in reports:
        for i in r.issues:
            cat_counts[i.category] += 1

    if cat_counts:
        lines.append("")
        lines.append("### Issues by Category")
        lines.append("")
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
            label = cat.replace("_", " ").title()
            lines.append(f"| {label} | {cnt} |")

    # -- Blank pages callout --
    if blank_pages:
        lines.append("")
        lines.append("### Blank/Stub Pages (Header + Footer Only)")
        lines.append("")
        for r in reports:
            if r.is_blank:
                title = f" - \"{r.title}\"" if r.title else ""
                lines.append(f"- **{r.url}**{title}")

    # -- HTTP error pages callout --
    if error_pages:
        lines.append("")
        lines.append("### Pages Returning HTTP Errors")
        lines.append("")
        for r in reports:
            if r.status_code >= 400:
                lines.append(f"- **{r.url}** - HTTP {r.status_code}")

    # -- Per-page detailed report --
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Per-Page Report")

    # Sort: pages with critical issues first, then warnings, then clean
    def sort_key(r):
        crits = sum(1 for i in r.issues if i.severity == "critical")
        warns = sum(1 for i in r.issues if i.severity == "warning")
        return (-crits, -warns, r.url)

    sorted_reports = sorted(reports, key=sort_key)

    for r in sorted_reports:
        lines.append("")
        lines.append(f"---")
        lines.append("")

        # Page header
        status_badge = ""
        if r.status_code >= 500:
            status_badge = " [SERVER ERROR]"
        elif r.status_code == 404:
            status_badge = " [404 NOT FOUND]"
        elif r.status_code >= 400:
            status_badge = f" [HTTP {r.status_code}]"
        elif r.is_blank:
            status_badge = " [BLANK PAGE]"

        title_str = f" - \"{r.title}\"" if r.title else ""
        lines.append(f"### {r.url}{title_str}{status_badge}")
        lines.append("")
        lines.append(f"- **Status:** {r.status_code} | "
                     f"**Load time:** {r.load_time_ms}ms | "
                     f"**Content:** {r.word_count} words | "
                     f"**Links:** {r.links_found} | "
                     f"**Images:** {r.images_found}")

        if not r.issues:
            lines.append(f"- No issues found")
            continue

        # Group issues by severity
        critical = [i for i in r.issues if i.severity == "critical"]
        warnings = [i for i in r.issues if i.severity == "warning"]
        info = [i for i in r.issues if i.severity == "info"]

        if critical:
            lines.append("")
            lines.append(f"**Critical Issues ({len(critical)}):**")
            for i in critical:
                lines.append(f"- CRITICAL: {i.message}")

        if warnings:
            lines.append("")
            lines.append(f"**Warnings ({len(warnings)}):**")
            for i in warnings:
                lines.append(f"- WARNING: {i.message}")

        if info:
            lines.append("")
            lines.append(f"**Info ({len(info)}):**")
            for i in info:
                lines.append(f"- INFO: {i.message}")

    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated on {time.strftime('%Y-%m-%d at %H:%M:%S')}*")
    lines.append("")

    return "\n".join(lines)


def generate_json_report(reports: list[PageReport], base_url: str,
                         duration: float) -> dict:
    """Generate structured JSON report."""
    return {
        "base_url": base_url,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "pages_crawled": len(reports),
        "duration_seconds": round(duration, 2),
        "summary": {
            "critical": sum(1 for r in reports for i in r.issues if i.severity == "critical"),
            "warnings": sum(1 for r in reports for i in r.issues if i.severity == "warning"),
            "info": sum(1 for r in reports for i in r.issues if i.severity == "info"),
            "blank_pages": sum(1 for r in reports if r.is_blank),
            "error_pages": sum(1 for r in reports if r.status_code >= 400),
            "clean_pages": sum(1 for r in reports if not r.issues),
        },
        "pages": [
            {
                "url": r.url,
                "title": r.title,
                "status_code": r.status_code,
                "load_time_ms": r.load_time_ms,
                "word_count": r.word_count,
                "is_blank": r.is_blank,
                "links_found": r.links_found,
                "images_found": r.images_found,
                "issues": [
                    {"severity": i.severity, "category": i.category,
                     "message": i.message}
                    for i in r.issues
                ],
            }
            for r in reports
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Crawl a staging site and generate a QA report for web designers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://staging.example.com
  %(prog)s https://staging.example.com --wp-user admin --wp-pass secret
  %(prog)s https://staging.example.com --max-pages 300 -o qa_report.md
  %(prog)s https://staging.example.com --no-external --no-verify-ssl
        """
    )
    parser.add_argument("url", help="The staging site URL to crawl")
    parser.add_argument("--max-pages", type=int, default=200,
                        help="Maximum pages to crawl (default: 200)")
    parser.add_argument("--timeout", type=int, default=15,
                        help="Request timeout in seconds (default: 15)")
    parser.add_argument("--no-verify-ssl", action="store_true",
                        help="Disable SSL certificate verification")
    parser.add_argument("--no-external", action="store_true",
                        help="Skip checking external links")
    parser.add_argument("--no-proxy", action="store_true",
                        help="Bypass system proxy settings")
    parser.add_argument("--wp-user", type=str, default=None,
                        help="WordPress username")
    parser.add_argument("--wp-pass", type=str, default=None,
                        help="WordPress password")
    parser.add_argument("-o", "--output", type=str, default="qa_report.md",
                        help="Output file path (default: qa_report.md)")
    parser.add_argument("--json", type=str, default=None,
                        help="Also save JSON report to this path")

    args = parser.parse_args()

    print(f"\n{'='*70}")
    print(f"  STAGING SITE QA REPORT GENERATOR")
    print(f"{'='*70}")
    print(f"  Target:      {args.url}")
    print(f"  Max pages:   {args.max_pages}")
    print(f"  Timeout:     {args.timeout}s")
    print(f"  External:    {'yes' if not args.no_external else 'no'}")
    print(f"{'='*70}\n")

    crawler = QAReportCrawler(
        base_url=args.url,
        max_pages=args.max_pages,
        timeout=args.timeout,
        verify_ssl=not args.no_verify_ssl,
        check_external=not args.no_external,
        no_proxy=args.no_proxy,
    )

    if args.wp_user and args.wp_pass:
        crawler.wp_login(args.wp_user, args.wp_pass)

    start = time.time()
    reports = crawler.crawl()
    duration = time.time() - start

    # Generate Markdown report
    md = generate_markdown_report(reports, args.url, duration)
    with open(args.output, "w") as f:
        f.write(md)
    print(f"\n  Markdown report saved to: {args.output}")

    # Generate JSON report
    if args.json:
        data = generate_json_report(reports, args.url, duration)
        with open(args.json, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  JSON report saved to:     {args.json}")

    # Print summary
    total_critical = sum(1 for r in reports for i in r.issues if i.severity == "critical")
    total_warnings = sum(1 for r in reports for i in r.issues if i.severity == "warning")
    blank = sum(1 for r in reports if r.is_blank)

    print(f"\n{'='*70}")
    print(f"  SUMMARY: {len(reports)} pages | "
          f"{total_critical} critical | {total_warnings} warnings | "
          f"{blank} blank pages")
    print(f"{'='*70}\n")

    sys.exit(1 if total_critical > 0 else 0)


if __name__ == "__main__":
    main()
