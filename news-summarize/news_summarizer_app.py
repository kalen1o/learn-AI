#!/usr/bin/env python3
"""
News Summarizer Application - Main application combining parser and AI summarizer
"""

import json
import logging
from typing import Dict, List, Optional
from news_parser import NewsParser
from ai_summarizer import AINewsSummarizer
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsSummarizerApp:
    """Main application for news summarization"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the news summarizer application"""
        self.parser = NewsParser()
        self.summarizer = AINewsSummarizer(api_key=openai_api_key)
        logger.info("News Summarizer Application initialized")
    
    def process_single_url(self, url: str, summary_style: str = "concise") -> Dict[str, any]:
        """Process a single news URL and generate summary"""
        try:
            logger.info(f"Processing URL: {url}")
            
            # Parse the news article
            article_data = self.parser.parse_news_url(url)
            
            if not article_data or not article_data.get('content'):
                raise ValueError("Failed to extract article content")
            
            logger.info(f"Extracted article: {len(article_data.get('content', ''))} characters")
            
            # Generate AI summary
            summary_data = self.summarizer.summarize_article(article_data, summary_style)
            
            logger.info(f"Generated summary with style: {summary_style}")
            
            return summary_data
            
        except Exception as e:
            logger.error(f"Failed to process URL {url}: {e}")
            raise
    
    def process_multiple_urls(self, urls: List[str], summary_style: str = "concise") -> List[Dict[str, any]]:
        """Process multiple news URLs and generate summaries"""
        results = []
        
        for i, url in enumerate(urls, 1):
            try:
                logger.info(f"Processing URL {i}/{len(urls)}: {url}")
                
                result = self.process_single_url(url, summary_style)
                results.append(result)
                
                # Be respectful to servers
                if i < len(urls):
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                results.append({
                    'error': str(e),
                    'url': url,
                    'status': 'failed'
                })
                continue
        
        return results
    
    def process_rss_feed(self, feed_url: str, summary_style: str = "concise", limit: int = 5) -> List[Dict[str, any]]:
        """Process RSS feed and generate summaries for articles"""
        try:
            logger.info(f"Processing RSS feed: {feed_url}")
            
            # Parse RSS feed
            articles = self.parser.parse_rss_feed(feed_url, limit)
            
            if not articles:
                raise ValueError("No articles found in RSS feed")
            
            logger.info(f"Found {len(articles)} articles in RSS feed")
            
            # Process each article
            results = []
            for i, article in enumerate(articles, 1):
                try:
                    logger.info(f"Processing RSS article {i}/{len(articles)}")
                    
                    # Get full article content
                    if article.get('link'):
                        full_article = self.parser.parse_news_url(article['link'])
                        
                        if full_article and full_article.get('content'):
                            # Generate summary
                            summary_data = self.summarizer.summarize_article(full_article, summary_style)
                            summary_data['rss_data'] = article
                            results.append(summary_data)
                        else:
                            # Use RSS summary if full article fails
                            summary_data = {
                                'original_article': article,
                                'summary': article.get('summary', 'No summary available'),
                                'key_points': [],
                                'sentiment': {'sentiment': 'neutral', 'confidence': 'low', 'explanation': 'Limited data'},
                                'insights': [],
                                'summary_style': summary_style,
                                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'rss_data': article
                            }
                            results.append(summary_data)
                    
                    # Be respectful to servers
                    if i < len(articles):
                        time.sleep(2)
                        
                except Exception as e:
                    logger.error(f"Failed to process RSS article: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to process RSS feed: {e}")
            raise
    
    def save_results(self, results: List[Dict[str, any]], filename: str = None) -> str:
        """Save results to JSON file"""
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"news_summaries_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Results saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise
    
    def print_summary(self, summary_data: Dict[str, any]):
        """Print a formatted summary to console"""
        print("\n" + "="*80)
        print("NEWS SUMMARY")
        print("="*80)
        
        # Original article info
        article = summary_data.get('original_article', {})
        print(f"Title: {article.get('title', 'N/A')}")
        print(f"URL: {article.get('url', 'N/A')}")
        print(f"Author: {article.get('author', 'N/A')}")
        print(f"Date: {article.get('date', 'N/A')}")
        print(f"Extraction Method: {article.get('method', 'N/A')}")
        
        print("\n" + "-"*80)
        print("AI GENERATED SUMMARY")
        print("-"*80)
        print(f"Style: {summary_data.get('summary_style', 'N/A')}")
        print(f"Generated: {summary_data.get('generated_at', 'N/A')}")
        
        print(f"\nSummary:\n{summary_data.get('summary', 'N/A')}")
        
        # Key points
        key_points = summary_data.get('key_points', [])
        if key_points:
            print(f"\nKey Points:")
            for i, point in enumerate(key_points, 1):
                print(f"  {i}. {point}")
        
        # Sentiment
        sentiment = summary_data.get('sentiment', {})
        if sentiment:
            print(f"\nSentiment Analysis:")
            print(f"  Overall: {sentiment.get('sentiment', 'N/A')}")
            print(f"  Confidence: {sentiment.get('confidence', 'N/A')}")
            print(f"  Explanation: {sentiment.get('explanation', 'N/A')}")
        
        # Insights
        insights = summary_data.get('insights', [])
        if insights:
            print(f"\nStrategic Insights:")
            for i, insight in enumerate(insights, 1):
                print(f"  {i}. {insight}")
        
        print("\n" + "="*80)

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='News Summarizer Application')
    parser.add_argument('--url', help='Single news URL to process')
    parser.add_argument('--urls', nargs='+', help='Multiple news URLs to process')
    parser.add_argument('--rss', help='RSS feed URL to process')
    parser.add_argument('--style', default='concise', 
                       choices=['concise', 'detailed', 'bullet_points', 'executive'],
                       help='Summary style')
    parser.add_argument('--limit', type=int, default=5, help='Number of RSS articles to process')
    parser.add_argument('--save', help='Save results to specified filename')
    parser.add_argument('--api-key', help='OpenAI API key')
    
    args = parser.parse_args()
    
    try:
        # Initialize app
        app = NewsSummarizerApp(openai_api_key=args.api_key)
        
        if args.url:
            # Process single URL
            result = app.process_single_url(args.url, args.style)
            app.print_summary(result)
            
            if args.save:
                app.save_results([result], args.save)
        
        elif args.urls:
            # Process multiple URLs
            results = app.process_multiple_urls(args.urls, args.style)
            
            for result in results:
                if 'error' not in result:
                    app.print_summary(result)
                else:
                    print(f"\nFailed to process {result['url']}: {result['error']}")
            
            if args.save:
                app.save_results(results, args.save)
        
        elif args.rss:
            # Process RSS feed
            results = app.process_rss_feed(args.rss, args.style, args.limit)
            
            for result in results:
                app.print_summary(result)
            
            if args.save:
                app.save_results(results, args.save)
        
        else:
            print("Please provide --url, --urls, or --rss argument")
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Application failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
