"""Website analysis tool using Playwright and various metrics."""

import asyncio
import json
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup

from website_prospector.models.types import Prospect, SiteAnalysis

logger = logging.getLogger(__name__)


class SiteAnalyzer:
    """Analyzes websites for outdatedness and improvement opportunities."""
    
    def __init__(self, screenshot_dir: Optional[Path] = None):
        self.screenshot_dir = screenshot_dir or Path(tempfile.gettempdir()) / "prospect_screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        
    async def analyze_site(
        self, 
        prospect: Prospect, 
        scoring_weights: Dict[str, float]
    ) -> Optional[SiteAnalysis]:
        """Perform comprehensive analysis of a website."""
        logger.info(f"Analyzing site: {prospect.url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            try:
                analysis = await self._analyze_with_browser(browser, prospect, scoring_weights)
                return analysis
            except Exception as e:
                logger.error(f"Failed to analyze {prospect.url}: {e}")
                return None
            finally:
                await browser.close()
    
    async def _analyze_with_browser(
        self, 
        browser: Browser, 
        prospect: Prospect, 
        scoring_weights: Dict[str, float]
    ) -> SiteAnalysis:
        """Analyze site using browser automation."""
        page = await browser.new_page()
        
        try:
            # Navigate to the site
            await page.goto(str(prospect.url), wait_until='networkidle', timeout=30000)
            
            # Take screenshot
            screenshot_path = await self._take_screenshot(page, prospect)
            
            # Get page content
            content = await page.content()
            html_soup = BeautifulSoup(content, 'html.parser')
            
            # Perform various analyses
            mobile_score = await self._analyze_mobile_responsiveness(page)
            performance_score = await self._analyze_performance(page)
            seo_score = self._analyze_seo(html_soup)
            security_score = await self._analyze_security(page)
            outdated_score = self._analyze_outdatedness(html_soup, content)
            
            # Calculate weighted overall score
            scores = {
                'mobile_responsiveness': mobile_score,
                'performance': performance_score,
                'seo': seo_score,
                'security': security_score,
                'outdated': outdated_score
            }
            
            overall_score = self._calculate_overall_score(scores, scoring_weights)
            
            # Identify improvement areas
            improvement_areas = self._identify_improvement_areas(scores)
            technical_issues = await self._identify_technical_issues(page, html_soup)
            
            return SiteAnalysis(
                url=prospect.url,
                outdated_score=outdated_score,
                mobile_score=mobile_score,
                performance_score=performance_score,
                seo_score=seo_score,
                security_score=security_score,
                overall_score=overall_score,
                improvement_areas=improvement_areas,
                technical_issues=technical_issues,
                screenshot_paths=[screenshot_path] if screenshot_path else []
            )
            
        finally:
            await page.close()
    
    async def _take_screenshot(self, page: Page, prospect: Prospect) -> Optional[str]:
        """Take a screenshot of the website."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(str(prospect.url)).netloc.replace('.', '_')
            filename = f"{domain}_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            await page.screenshot(path=str(filepath), full_page=True)
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    async def _analyze_mobile_responsiveness(self, page: Page) -> float:
        """Analyze mobile responsiveness."""
        try:
            # Test on mobile viewport
            await page.set_viewport_size({'width': 375, 'height': 667})
            await page.wait_for_timeout(1000)
            
            # Check for mobile-friendly elements
            mobile_indicators = await page.evaluate("""
                () => {
                    const viewport = document.querySelector('meta[name="viewport"]');
                    const mediaQueries = Array.from(document.styleSheets).some(sheet => {
                        try {
                            return Array.from(sheet.cssRules).some(rule => 
                                rule.media && rule.media.mediaText.includes('max-width')
                            );
                        } catch (e) { return false; }
                    });
                    
                    return {
                        hasViewportMeta: !!viewport,
                        hasMediaQueries: mediaQueries,
                        bodyWidth: document.body.scrollWidth,
                        viewportWidth: window.innerWidth
                    };
                }
            """)
            
            score = 0.0
            if mobile_indicators['hasViewportMeta']:
                score += 0.4
            if mobile_indicators['hasMediaQueries']:
                score += 0.4
            if mobile_indicators['bodyWidth'] <= mobile_indicators['viewportWidth'] * 1.1:
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Mobile analysis failed: {e}")
            return 0.5  # Default neutral score
    
    async def _analyze_performance(self, page: Page) -> float:
        """Analyze website performance."""
        try:
            # Measure page load metrics
            metrics = await page.evaluate("""
                () => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    const paintEntries = performance.getEntriesByType('paint');
                    
                    return {
                        loadTime: perfData ? perfData.loadEventEnd - perfData.loadEventStart : 0,
                        domContentLoaded: perfData ? perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart : 0,
                        firstPaint: paintEntries.find(entry => entry.name === 'first-paint')?.startTime || 0,
                        imageCount: document.images.length,
                        scriptCount: document.scripts.length
                    };
                }
            """)
            
            score = 1.0
            
            # Penalize slow load times
            if metrics['loadTime'] > 3000:
                score -= 0.3
            elif metrics['loadTime'] > 1500:
                score -= 0.1
            
            # Penalize slow first paint
            if metrics['firstPaint'] > 2000:
                score -= 0.2
            
            # Penalize excessive resources
            if metrics['imageCount'] > 50:
                score -= 0.1
            if metrics['scriptCount'] > 20:
                score -= 0.1
            
            return max(score, 0.0)
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return 0.5
    
    def _analyze_seo(self, soup: BeautifulSoup) -> float:
        """Analyze SEO factors."""
        score = 0.0
        
        # Title tag
        title = soup.find('title')
        if title and title.get_text(strip=True):
            score += 0.2
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            score += 0.2
        
        # Headings structure
        h1_tags = soup.find_all('h1')
        if h1_tags and len(h1_tags) == 1:
            score += 0.15
        elif h1_tags:
            score += 0.1
        
        if soup.find_all(['h2', 'h3']):
            score += 0.1
        
        # Alt tags on images
        images = soup.find_all('img')
        if images:
            images_with_alt = [img for img in images if img.get('alt')]
            alt_ratio = len(images_with_alt) / len(images)
            score += 0.15 * alt_ratio
        else:
            score += 0.15  # No images to worry about
        
        # Internal linking
        internal_links = soup.find_all('a', href=True)
        if len(internal_links) > 5:
            score += 0.1
        
        # Schema markup
        if soup.find_all(attrs={'itemtype': True}) or soup.find_all('script', type='application/ld+json'):
            score += 0.1
        
        return min(score, 1.0)
    
    async def _analyze_security(self, page: Page) -> float:
        """Analyze security factors."""
        try:
            url = page.url
            score = 0.0
            
            # HTTPS check
            if url.startswith('https://'):
                score += 0.5
            
            # Check for security headers (simplified)
            response = await page.evaluate("""
                () => {
                    // This is a simplified check
                    // In production, you'd want to check actual HTTP headers
                    return {
                        hasSecurityHeaders: document.querySelector('meta[http-equiv="Content-Security-Policy"]') !== null
                    };
                }
            """)
            
            if response.get('hasSecurityHeaders'):
                score += 0.2
            
            # Form security (simplified check)
            forms = await page.query_selector_all('form')
            if forms:
                secure_forms = 0
                for form in forms:
                    action = await form.get_attribute('action')
                    if not action or action.startswith('https://') or action.startswith('/'):
                        secure_forms += 1
                
                if secure_forms == len(forms):
                    score += 0.3
                else:
                    score += 0.1
            else:
                score += 0.3  # No forms to worry about
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            return 0.5
    
    def _analyze_outdatedness(self, soup: BeautifulSoup, content: str) -> float:
        """Analyze how outdated the website appears."""
        outdated_score = 0.0
        
        # Check for outdated design patterns
        outdated_indicators = [
            'table-based layout',
            'font tags',
            'center tags',
            'marquee',
            'blink',
            'frameset',
        ]
        
        content_lower = content.lower()
        for indicator in outdated_indicators:
            if indicator.replace(' ', '') in content_lower.replace(' ', ''):
                outdated_score += 0.1
        
        # Check for inline styles (often indicates older development)
        inline_styles = soup.find_all(attrs={'style': True})
        if len(inline_styles) > 10:
            outdated_score += 0.2
        
        # Check for Flash content
        if soup.find_all(['embed', 'object']) or 'flash' in content_lower:
            outdated_score += 0.3
        
        # Check for outdated meta tags
        if soup.find('meta', attrs={'name': 'generator', 'content': lambda x: x and 'frontpage' in x.lower()}):
            outdated_score += 0.2
        
        # Check copyright dates
        import re
        copyright_years = re.findall(r'copyright.*?(\d{4})', content_lower)
        current_year = datetime.now().year
        
        for year_str in copyright_years:
            year = int(year_str)
            if current_year - year > 3:
                outdated_score += 0.2
                break
        
        return min(outdated_score, 1.0)
    
    def _calculate_overall_score(
        self, 
        scores: Dict[str, float], 
        weights: Dict[str, float]
    ) -> float:
        """Calculate weighted overall score."""
        total_score = 0.0
        total_weight = 0.0
        
        for metric, score in scores.items():
            weight = weights.get(metric, 0.0)
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _identify_improvement_areas(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas that need improvement based on scores."""
        improvements = []
        threshold = 0.6
        
        if scores.get('mobile_responsiveness', 1.0) < threshold:
            improvements.append('mobile_responsiveness')
        
        if scores.get('performance', 1.0) < threshold:
            improvements.append('page_speed_optimization')
        
        if scores.get('seo', 1.0) < threshold:
            improvements.append('search_engine_optimization')
        
        if scores.get('security', 1.0) < threshold:
            improvements.append('security_enhancements')
        
        if scores.get('outdated', 0.0) > 0.4:
            improvements.append('modern_design_update')
        
        return improvements
    
    async def _identify_technical_issues(
        self, 
        page: Page, 
        soup: BeautifulSoup
    ) -> List[str]:
        """Identify specific technical issues."""
        issues = []
        
        try:
            # Check for broken images
            broken_images = await page.evaluate("""
                () => {
                    return Array.from(document.images).filter(img => 
                        !img.complete || img.naturalWidth === 0
                    ).length;
                }
            """)
            
            if broken_images > 0:
                issues.append(f"{broken_images} broken images detected")
            
            # Check for missing alt tags
            images_without_alt = soup.find_all('img', alt=False)
            if images_without_alt:
                issues.append(f"{len(images_without_alt)} images missing alt text")
            
            # Check for inline CSS/JS
            inline_styles = len(soup.find_all(attrs={'style': True}))
            if inline_styles > 5:
                issues.append(f"Excessive inline styles ({inline_styles} elements)")
            
            # Check for missing meta tags
            if not soup.find('title'):
                issues.append("Missing page title")
            
            if not soup.find('meta', attrs={'name': 'description'}):
                issues.append("Missing meta description")
            
            # Check for external resources without HTTPS
            external_resources = soup.find_all(['link', 'script', 'img'], src=True)
            http_resources = [r for r in external_resources if r.get('src', '').startswith('http://')]
            if http_resources:
                issues.append(f"{len(http_resources)} resources loaded over HTTP")
            
            return issues
            
        except Exception as e:
            logger.error(f"Technical issues analysis failed: {e}")
            return ["Could not analyze technical issues"]