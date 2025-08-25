#!/usr/bin/env python3
"""
Example usage of the News Summarizer Application
"""

from news_summarizer_app import NewsSummarizerApp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_single_url():
    """Example: Process a single news URL"""
    print("=== Example: Single URL Processing ===")
    
    # Example news URL (replace with actual URL)
    news_url = "https://www.bbc.com/news/business-12345678"
    
    try:
        # Initialize the app
        app = NewsSummarizerApp()
        
        # Process the URL
        result = app.process_single_url(news_url, summary_style="concise")
        
        # Print the summary
        app.print_summary(result)
        
        # Save results
        filename = app.save_results([result])
        print(f"\nResults saved to: {filename}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_multiple_urls():
    """Example: Process multiple news URLs"""
    print("=== Example: Multiple URLs Processing ===")
    
    # Example news URLs (replace with actual URLs)
    news_urls = [
        "https://www.bbc.com/news/business-12345678",
        "https://www.cnn.com/business/2024/01/01/example-article",
        "https://www.reuters.com/business/example-article"
    ]
    
    try:
        # Initialize the app
        app = NewsSummarizerApp()
        
        # Process multiple URLs
        results = app.process_multiple_urls(news_urls, summary_style="detailed")
        
        # Print summaries
        for result in results:
            if 'error' not in result:
                app.print_summary(result)
            else:
                print(f"\nFailed to process {result['url']}: {result['error']}")
        
        # Save results
        filename = app.save_results(results)
        print(f"\nResults saved to: {filename}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_rss_feed():
    """Example: Process RSS feed"""
    print("=== Example: RSS Feed Processing ===")
    
    # Example RSS feed URL (replace with actual RSS feed)
    rss_url = "https://feeds.bbci.co.uk/news/business/rss.xml"
    
    try:
        # Initialize the app
        app = NewsSummarizerApp()
        
        # Process RSS feed
        results = app.process_rss_feed(rss_url, summary_style="executive", limit=3)
        
        # Print summaries
        for result in results:
            app.print_summary(result)
        
        # Save results
        filename = app.save_results(results)
        print(f"\nResults saved to: {filename}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_different_styles():
    """Example: Different summary styles"""
    print("=== Example: Different Summary Styles ===")
    
    news_url = "https://www.bbc.com/news/business-12345678"
    styles = ["concise", "detailed", "bullet_points", "executive"]
    
    try:
        app = NewsSummarizerApp()
        
        for style in styles:
            print(f"\n--- {style.upper()} STYLE ---")
            result = app.process_single_url(news_url, summary_style=style)
            print(f"Summary: {result.get('summary', 'N/A')[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key before running the examples.")
        print("You can create a .env file with: OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    print("News Summarizer Application - Example Usage")
    print("=" * 50)
    
    # Run examples
    try:
        example_single_url()
        print("\n" + "=" * 50)
        
        example_multiple_urls()
        print("\n" + "=" * 50)
        
        example_rss_feed()
        print("\n" + "=" * 50)
        
        example_different_styles()
        
    except Exception as e:
        print(f"Examples failed: {e}")
    
    print("\n" + "=" * 50)
    print("Examples completed!")
