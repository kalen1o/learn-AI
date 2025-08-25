#!/usr/bin/env python3
"""
News Parser - Extract and parse content from various news websites
"""

import requests
from bs4 import BeautifulSoup
from newspaper import Article
import feedparser
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsParser:
    """Parse news content from various websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common news selectors for different websites
        self.selectors = {
            'generic': {
                'title': ['h1', 'h2', '.title', '.headline', '[class*="title"]', '[class*="headline"]'],
                'content': ['article', '.content', '.article-content', '.story-content', '.post-content', '[class*="content"]'],
                'summary': ['.summary', '.excerpt', '.description', '[class*="summary"]'],
                'author': ['.author', '.byline', '[class*="author"]', '[class*="byline"]'],
                'date': ['.date', '.time', '.published', '[class*="date"]', '[class*="time"]']
            },
            'bbc': {
                'title': ['h1', '.story-body__h1'],
                'content': ['.story-body__inner', '.story-body__introduction'],
                'summary': ['.story-body__introduction'],
                'author': ['.byline__name'],
                'date': ['.date', '.timestamp']
            },
            'cnn': {
                'title': ['.headline__text', 'h1'],
                'content': ['.article__content', '.l-container'],
                'summary': ['.article__subtitle'],
                'author': ['.byline__name'],
                'date': ['.timestamp']
            },
            'reuters': {
                'title': ['h1', '.article-header__title'],
                'content': ['.article-content__content__2gQno', '.article-body__content__17Yit'],
                'summary': ['.article-header__summary__1l7fm'],
                'author': ['.article-header__author__1l7fm'],
                'date': ['.article-header__timestamp__1l7fm']
            }
        }
    
    def detect_website_type(self, url: str) -> str:
        """Detect the type of website based on URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'bbc' in domain:
            return 'bbc'
        elif 'cnn' in domain:
            return 'cnn'
        elif 'reuters' in domain:
            return 'reuters'
        else:
            return 'generic'
    
    def extract_with_newspaper(self, url: str) -> Dict[str, str]:
        """Extract content using newspaper3k library"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                'title': article.title or '',
                'content': article.text or '',
                'summary': article.summary or '',
                'author': ', '.join(article.authors) if article.authors else '',
                'date': str(article.publish_date) if article.publish_date else '',
                'keywords': ', '.join(article.keywords) if article.keywords else '',
                'method': 'newspaper3k'
            }
        except Exception as e:
            logger.warning(f"Newspaper3k failed for {url}: {e}")
            return {}
    
    def extract_with_beautifulsoup(self, url: str, website_type: str = 'generic') -> Dict[str, str]:
        """Extract content using BeautifulSoup with custom selectors"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            selectors = self.selectors[website_type]
            
            # Extract title
            title = ''
            for selector in selectors['title']:
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    break
            
            # Extract content
            content = ''
            for selector in selectors['content']:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text(strip=True) for elem in elements])
                    break
            
            # Extract summary
            summary = ''
            for selector in selectors['summary']:
                element = soup.select_one(selector)
                if element:
                    summary = element.get_text(strip=True)
                    break
            
            # Extract author
            author = ''
            for selector in selectors['author']:
                element = soup.select_one(selector)
                if element:
                    author = element.get_text(strip=True)
                    break
            
            # Extract date
            date = ''
            for selector in selectors['date']:
                element = soup.select_one(selector)
                if element:
                    date = element.get_text(strip=True)
                    break
            
            # Clean up content
            content = self.clean_text(content)
            summary = self.clean_text(summary)
            
            return {
                'title': title,
                'content': content,
                'summary': summary,
                'author': author,
                'date': date,
                'method': 'beautifulsoup'
            }
            
        except Exception as e:
            logger.error(f"BeautifulSoup extraction failed for {url}: {e}")
            return {}
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ''
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common unwanted patterns
        text = re.sub(r'Share this article|Follow us|Subscribe|Newsletter', '', text, flags=re.IGNORECASE)
        
        # Remove social media links
        text = re.sub(r'https?://[^\s]+', '', text)
        
        return text.strip()
    
    def parse_news_url(self, url: str) -> Dict[str, str]:
        """Main method to parse news from URL"""
        logger.info(f"Parsing news from: {url}")
        
        # Detect website type
        website_type = self.detect_website_type(url)
        
        # Try newspaper3k first (usually more reliable)
        result = self.extract_with_newspaper(url)
        
        # If newspaper3k fails or returns minimal content, try BeautifulSoup
        if not result or len(result.get('content', '')) < 100:
            logger.info("Newspaper3k returned minimal content, trying BeautifulSoup...")
            bs_result = self.extract_with_beautifulsoup(url, website_type)
            
            if bs_result and len(bs_result.get('content', '')) > len(result.get('content', '')):
                result = bs_result
        
        # Add metadata
        result['url'] = url
        result['website_type'] = website_type
        result['extraction_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        return result
    
    def parse_rss_feed(self, feed_url: str, limit: int = 10) -> List[Dict[str, str]]:
        """Parse RSS feed and extract articles"""
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:limit]:
                article = {
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'author': entry.get('author', '')
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            logger.error(f"RSS parsing failed for {feed_url}: {e}")
            return []
    
    def batch_parse_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """Parse multiple URLs in batch"""
        results = []
        
        for url in urls:
            try:
                result = self.parse_news_url(url)
                if result:
                    results.append(result)
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                logger.error(f"Failed to parse {url}: {e}")
                continue
        
        return results
