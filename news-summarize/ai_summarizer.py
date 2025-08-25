#!/usr/bin/env python3
"""
AI News Summarizer - Generate summaries using OpenAI API
"""

import os
import openai
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AINewsSummarizer:
    """Generate AI-powered summaries of news content"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI summarizer"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass as parameter.")
        
        # Initialize OpenAI client
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def generate_summary(self, content: str, style: str = "concise", max_length: int = 200) -> str:
        """Generate a summary of the given content"""
        try:
            # Determine prompt based on style
            if style == "concise":
                prompt = f"""Please provide a concise summary of the following news article in approximately {max_length} words. Focus on the main facts, key points, and essential information.

Article content:
{content}

Summary:"""
            
            elif style == "detailed":
                prompt = f"""Please provide a detailed summary of the following news article in approximately {max_length} words. Include main facts, context, key quotes, and implications.

Article content:
{content}

Summary:"""
            
            elif style == "bullet_points":
                prompt = f"""Please provide a summary of the following news article in bullet point format. Focus on main facts, key points, and important details.

Article content:
{content}

Summary:"""
            
            elif style == "executive":
                prompt = f"""Please provide an executive summary of the following news article in approximately {max_length} words. Focus on business implications, key decisions, and strategic insights.

Article content:
{content}

Summary:"""
            
            else:
                raise ValueError("Style must be 'concise', 'detailed', 'bullet_points', or 'executive'")
            
            # Generate summary using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional news analyst and summarizer. Provide accurate, objective, and well-structured summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length * 2,  # Approximate token limit
                temperature=0.3,
                top_p=0.9
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated {style} summary: {len(summary)} characters")
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            raise Exception(f"Summary generation failed: {str(e)}")
    
    def generate_key_points(self, content: str, num_points: int = 5) -> List[str]:
        """Extract key points from the content"""
        try:
            prompt = f"""Please extract {num_points} key points from the following news article. Each point should be a concise, factual statement.

Article content:
{content}

Key points:"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a news analyst. Extract key factual points from news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            key_points_text = response.choices[0].message.content.strip()
            
            # Parse key points (assuming they're numbered or bulleted)
            points = []
            for line in key_points_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-') or line.startswith('*')):
                    # Remove numbering/bullets and clean up
                    clean_point = re.sub(r'^[\d•\-*\.\s]+', '', line).strip()
                    if clean_point:
                        points.append(clean_point)
            
            # If parsing failed, split by sentences
            if len(points) < num_points:
                sentences = re.split(r'[.!?]+', key_points_text)
                points = [s.strip() for s in sentences if len(s.strip()) > 20][:num_points]
            
            return points[:num_points]
            
        except Exception as e:
            logger.error(f"Failed to generate key points: {e}")
            return []
    
    def analyze_sentiment(self, content: str) -> Dict[str, str]:
        """Analyze the sentiment of the news content"""
        try:
            prompt = f"""Please analyze the sentiment of the following news article. Provide:
1. Overall sentiment (positive, negative, neutral, or mixed)
2. Confidence level (high, medium, or low)
3. Brief explanation

Article content:
{content}

Analysis:"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Analyze news articles objectively."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse the analysis
            sentiment = "neutral"
            confidence = "medium"
            explanation = analysis_text
            
            # Try to extract sentiment and confidence
            if "positive" in analysis_text.lower():
                sentiment = "positive"
            elif "negative" in analysis_text.lower():
                sentiment = "negative"
            elif "mixed" in analysis_text.lower():
                sentiment = "mixed"
            
            if "high" in analysis_text.lower():
                confidence = "high"
            elif "low" in analysis_text.lower():
                confidence = "low"
            
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "explanation": explanation
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            return {
                "sentiment": "neutral",
                "confidence": "low",
                "explanation": "Sentiment analysis failed"
            }
    
    def generate_insights(self, content: str) -> List[str]:
        """Generate insights and implications from the news content"""
        try:
            prompt = f"""Please provide 3-5 key insights or implications from the following news article. Focus on:
- Business implications
- Market impact
- Strategic considerations
- Future trends

Article content:
{content}

Insights:"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a business analyst. Provide strategic insights from news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.4
            )
            
            insights_text = response.choices[0].message.content.strip()
            
            # Parse insights
            insights = []
            for line in insights_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-') or line.startswith('*')):
                    clean_insight = re.sub(r'^[\d•\-*\.\s]+', '', line).strip()
                    if clean_insight:
                        insights.append(clean_insight)
            
            return insights[:5]
            
        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")
            return []
    
    def summarize_article(self, article_data: Dict[str, str], style: str = "concise") -> Dict[str, any]:
        """Generate comprehensive summary of an article"""
        try:
            content = article_data.get('content', '')
            if not content or len(content) < 50:
                raise ValueError("Article content is too short or empty")
            
            # Generate summary
            summary = self.generate_summary(content, style)
            
            # Generate key points
            key_points = self.generate_key_points(content)
            
            # Analyze sentiment
            sentiment = self.analyze_sentiment(content)
            
            # Generate insights
            insights = self.generate_insights(content)
            
            return {
                'original_article': article_data,
                'summary': summary,
                'key_points': key_points,
                'sentiment': sentiment,
                'insights': insights,
                'summary_style': style,
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.error(f"Failed to summarize article: {e}")
            raise Exception(f"Article summarization failed: {str(e)}")

# Import missing modules
import re
import time
