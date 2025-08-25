# News Summarizer Application

A powerful Python application that extracts content from news websites and generates AI-powered summaries using OpenAI's GPT models.

## Features

- **Multi-source News Parsing**: Extract content from various news websites including BBC, CNN, Reuters, and generic news sites
- **AI-powered Summarization**: Generate summaries using OpenAI's GPT-3.5-turbo model
- **Multiple Summary Styles**: Concise, detailed, bullet points, and executive summaries
- **Sentiment Analysis**: Analyze the emotional tone of news articles
- **Key Points Extraction**: Identify and extract main facts and key points
- **Strategic Insights**: Generate business and strategic implications
- **RSS Feed Support**: Process RSS feeds and summarize multiple articles
- **Batch Processing**: Handle multiple URLs efficiently
- **Export Results**: Save summaries to JSON files

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd news-summarize
```

2. **Set up virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Command Line Interface

#### Process a single news URL:
```bash
python news_summarizer_app.py --url "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style concise
```

#### Process multiple URLs:
```bash
python news_summarizer_app.py --urls "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" "https://dev.to/anuradha9712/building-your-first-cli-tool-98h" --style detailed
```

#### Process RSS feed:
```bash
python news_summarizer_app.py --rss "https://feeds.bbci.co.uk/news/business/rss.xml" --limit 5 --style executive
```

#### Save results to file:
```bash
python news_summarizer_app.py --url "https://dev.to/om_shree_0709/leetcode-3197-covering-all-ones-with-3-rectangles-c-python-java-40fd" --save "my_summary.json"
```

### Python API

#### Basic Usage:
```python
from news_summarizer_app import NewsSummarizerApp

# Initialize the app
app = NewsSummarizerApp()

# Process a single URL
result = app.process_single_url("https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb", summary_style="concise")

# Print the summary
app.print_summary(result)

# Save results
app.save_results([result])
```

#### Process Multiple URLs:
```python
urls = ["https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb", "https://dev.to/anuradha9712/building-your-first-cli-tool-98h", "https://dev.to/om_shree_0709/leetcode-3197-covering-all-ones-with-3-rectangles-c-python-java-40fd"]
results = app.process_multiple_urls(urls, summary_style="detailed")

for result in results:
    if 'error' not in result:
        app.print_summary(result)
```

#### Process RSS Feed:
```python
results = app.process_rss_feed("https://dev.to/feed", limit=5)
```

## Summary Styles

- **concise**: Brief summary focusing on main facts (default)
- **detailed**: Comprehensive summary with context and implications
- **bullet_points**: Structured summary in bullet point format
- **executive**: Business-focused summary with strategic insights

## Supported News Sources

The application automatically detects and optimizes parsing for:

- **BBC News**: Optimized selectors for BBC articles
- **CNN**: Custom parsing for CNN content
- **Reuters**: Specialized extraction for Reuters articles
- **Generic News Sites**: Universal selectors for other news sources

## Output Format

Each summary includes:

```json
{
  "original_article": {
    "title": "Article title",
    "content": "Full article content",
    "author": "Author name",
    "date": "Publication date",
    "url": "Source URL",
    "method": "Extraction method used"
  },
  "summary": "AI-generated summary",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "sentiment": {
    "sentiment": "positive/negative/neutral/mixed",
    "confidence": "high/medium/low",
    "explanation": "Sentiment analysis explanation"
  },
  "insights": ["Insight 1", "Insight 2", "Insight 3"],
  "summary_style": "concise",
  "generated_at": "2024-01-01 12:00:00"
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization

You can customize the news parsing by modifying the selectors in `news_parser.py`:

```python
self.selectors = {
    'your_site': {
        'title': ['.your-title-selector'],
        'content': ['.your-content-selector'],
        'summary': ['.your-summary-selector'],
        'author': ['.your-author-selector'],
        'date': ['.your-date-selector']
    }
}
```

## Error Handling

The application includes comprehensive error handling:

- **Network errors**: Automatic retry and fallback methods
- **Parsing failures**: Multiple extraction strategies
- **API errors**: Graceful degradation and user feedback
- **Rate limiting**: Built-in delays to respect server limits

## Performance Considerations

- **Rate limiting**: 2-second delay between requests to be respectful to servers
- **Timeout handling**: 10-second timeout for web requests
- **Fallback methods**: Multiple extraction strategies for reliability
- **Batch processing**: Efficient handling of multiple URLs

## Examples

See `example_usage.py` for comprehensive usage examples:

```bash
python example_usage.py
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure your API key is set in the `.env` file
2. **Parsing Failures**: Some websites may block automated access
3. **Rate Limiting**: The app includes delays to respect server limits
4. **Content Extraction**: If newspaper3k fails, BeautifulSoup fallback is used
5. **lxml Import Error**: If you see "lxml.html.clean module is now a separate project" error, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This will install `lxml-html-clean` which is required for HTML cleaning operations.

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Dependencies

- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML parsing and extraction
- **newspaper3k**: Advanced article extraction
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management
- **feedparser**: RSS feed parsing
- **nltk**: Natural language processing utilities

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the examples
3. Open an issue on GitHub
4. Check the logs for detailed error information

## Roadmap

- [ ] Web interface for easier usage
- [ ] Support for more news sources
- [ ] Custom summary templates
- [ ] Multi-language support
- [ ] Real-time news monitoring
- [ ] Integration with news APIs
