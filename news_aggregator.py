import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
import hashlib
import json
import os
from typing import List, Dict, Any
import asyncio
import httpx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import openai
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import re

load_dotenv()

class NewsAggregator:
    def __init__(self):
        self.db_path = "news_database.db"
        self.similarity_threshold = 0.7
        self.init_database()
        
        # OpenAI API key for summarization
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # News sources configuration
        self.automotive_companies = {
            "Tesla": {
                "website": "https://www.tesla.com/news",
                "rss": None
            },
            "Ford": {
                "website": "https://media.ford.com",
                "rss": "https://media.ford.com/content/fordmedia/fna/us/en/news.rss"
            },
            "GM": {
                "website": "https://news.gm.com",
                "rss": "https://news.gm.com/rss"
            },
            "Toyota": {
                "website": "https://global.toyota/en/newsroom",
                "rss": None
            },
            "BMW": {
                "website": "https://www.press.bmwgroup.com",
                "rss": None
            },
            "Mercedes": {
                "website": "https://media.mercedes-benz.com",
                "rss": None
            },
            "Volkswagen": {
                "website": "https://www.volkswagen-newsroom.com",
                "rss": None
            }
        }
        
        self.news_sources = {
            "Automotive News": "https://feeds.feedburner.com/autonews/AutoNews",
            "Motor Trend": "https://www.motortrend.com/feeds/all/",
            "Car and Driver": "https://www.caranddriver.com/rss/all/",
            "Autoblog": "https://www.autoblog.com/rss.xml",
            "Reuters Autos": "https://feeds.reuters.com/reuters/INautos",
            "Bloomberg Autos": "https://feeds.bloomberg.com/markets/news.rss"
        }
        
        self.regulatory_sources = {
            "NHTSA": {
                "base_url": "https://www.nhtsa.gov",
                "news_url": "https://www.nhtsa.gov/news",
                "recalls_api": "https://api.nhtsa.gov/recalls/recallsByVehicle"
            },
            "IIHS": {
                "base_url": "https://www.iihs.org",
                "news_url": "https://www.iihs.org/news"
            },
            "EPA": {
                "base_url": "https://www.epa.gov",
                "news_url": "https://www.epa.gov/newsroom"
            }
        }

    def init_database(self):
        """Initialize SQLite database for storing news articles"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                summary TEXT,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                url TEXT,
                published_date DATETIME,
                scraped_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                content_hash TEXT UNIQUE,
                similarity_hash TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def calculate_content_hash(self, content: str) -> str:
        """Calculate hash for content deduplication"""
        return hashlib.md5(content.encode()).hexdigest()

    def calculate_similarity_hash(self, title: str, content: str) -> str:
        """Calculate similarity hash for near-duplicate detection"""
        combined = f"{title} {content[:500]}"  # Use first 500 chars
        return hashlib.sha256(combined.lower().encode()).hexdigest()

    async def scrape_company_news(self, company: str, config: Dict) -> List[Dict]:
        """Scrape news from automotive company websites"""
        articles = []
        
        try:
            if config.get("rss"):
                # Use RSS feed if available
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(config["rss"], timeout=10.0)
                        articles.extend(self.parse_rss_content(response.text, company, "Company News"))
                except Exception as e:
                    print(f"Error fetching RSS for {company}: {e}")
            else:
                # Scrape website directly
                async with httpx.AsyncClient() as client:
                    response = await client.get(config["website"], timeout=10.0)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Generic news extraction (this would need customization per site)
                    news_items = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                        keyword in x.lower() for keyword in ['news', 'press', 'release', 'article']
                    ))[:10]
                    
                    for item in news_items:
                        title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                        if title_elem:
                            article = {
                                "title": title_elem.get_text().strip(),
                                "content": item.get_text().strip()[:1000],
                                "url": config["website"],
                                "published_date": datetime.now().isoformat(),
                                "source": company,
                                "category": "Company News"
                            }
                            articles.append(article)
        
        except Exception as e:
            print(f"Error scraping {company}: {e}")
        
        return articles

    async def scrape_news_sources(self) -> List[Dict]:
        """Scrape automotive news from various news organizations"""
        articles = []
        
        for source_name, rss_url in self.news_sources.items():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(rss_url, timeout=10.0)
                    rss_articles = self.parse_rss_content(response.text, source_name, "Industry News")
                    # Filter for automotive-related content
                    for article in rss_articles:
                        if self.is_automotive_related(article["title"] + " " + article.get("content", "")):
                            articles.append(article)
            except Exception as e:
                print(f"Error scraping {source_name}: {e}")
        
        return articles

    async def scrape_regulatory_news(self) -> List[Dict]:
        """Scrape regulatory information from government sources"""
        articles = []
        
        for agency, config in self.regulatory_sources.items():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(config["news_url"], timeout=10.0)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Generic regulatory news extraction
                    news_items = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                        keyword in x.lower() for keyword in ['news', 'press', 'release', 'recall']
                    ))[:10]
                    
                    for item in news_items:
                        title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                        if title_elem and self.is_automotive_related(title_elem.get_text()):
                            article = {
                                "title": title_elem.get_text().strip(),
                                "content": item.get_text().strip()[:1000],
                                "url": config["news_url"],
                                "published_date": datetime.now().isoformat(),
                                "source": agency,
                                "category": "Regulatory"
                            }
                            articles.append(article)
            
            except Exception as e:
                print(f"Error scraping {agency}: {e}")
        
        return articles

    def is_automotive_related(self, text: str) -> bool:
        """Check if text is automotive-related"""
        automotive_keywords = [
            'car', 'auto', 'vehicle', 'truck', 'suv', 'electric', 'hybrid',
            'tesla', 'ford', 'gm', 'toyota', 'bmw', 'mercedes', 'volkswagen',
            'recall', 'safety', 'crash', 'nhtsa', 'iihs', 'epa', 'emissions',
            'autonomous', 'self-driving', 'ev', 'battery', 'charging'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in automotive_keywords)

    def is_duplicate(self, article: Dict) -> bool:
        """Check if article is a duplicate using content and similarity hashing"""
        content_hash = self.calculate_content_hash(article["content"])
        similarity_hash = self.calculate_similarity_hash(article["title"], article["content"])
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check exact duplicate
        cursor.execute("SELECT id FROM articles WHERE content_hash = ?", (content_hash,))
        if cursor.fetchone():
            conn.close()
            return True
        
        # Check similar articles using TF-IDF and cosine similarity
        cursor.execute("""
            SELECT title, content FROM articles 
            WHERE category = ? AND scraped_date > datetime('now', '-7 days')
        """, (article["category"],))
        
        existing_articles = cursor.fetchall()
        conn.close()
        
        if existing_articles:
            # Prepare texts for similarity comparison
            new_text = f"{article['title']} {article['content']}"
            existing_texts = [f"{title} {content}" for title, content in existing_articles]
            all_texts = existing_texts + [new_text]
            
            # Calculate TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate cosine similarity with existing articles
            new_vector = tfidf_matrix[-1]
            similarities = cosine_similarity(new_vector, tfidf_matrix[:-1]).flatten()
            
            # Check if any similarity exceeds threshold
            if max(similarities.flatten()) > self.similarity_threshold:
                return True
        
        return False

    async def generate_summary(self, article: Dict) -> str:
        """Generate TL;DR summary using OpenAI GPT"""
        try:
            if not openai.api_key:
                # Fallback to simple TextBlob summarization
                blob = TextBlob(article["content"])
                sentences = blob.sentences
                if len(sentences) > 3:
                    return str(sentences[0]) + " " + str(sentences[1]) + " " + str(sentences[2])
                return article["content"][:200] + "..."
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a news summarizer. Create concise TL;DR summaries of automotive news articles in 2-3 sentences."},
                    {"role": "user", "content": f"Title: {article['title']}\n\nContent: {article['content'][:1500]}"}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback summary
            return article["content"][:200] + "..."

    def save_article(self, article: Dict):
        """Save article to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        content_hash = self.calculate_content_hash(article["content"])
        similarity_hash = self.calculate_similarity_hash(article["title"], article["content"])
        
        cursor.execute('''
            INSERT INTO articles (title, content, summary, source, category, url, 
                                published_date, content_hash, similarity_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article["title"],
            article["content"],
            article.get("summary", ""),
            article["source"],
            article["category"],
            article.get("url", ""),
            article.get("published_date", datetime.now().isoformat()),
            content_hash,
            similarity_hash
        ))
        
        conn.commit()
        conn.close()

    async def collect_and_process_news(self):
        """Main method to collect, deduplicate, and process all news"""
        print("Starting news collection...")
        
        all_articles = []
        
        # Collect from all sources
        tasks = []
        
        # Company news
        for company, config in self.automotive_companies.items():
            tasks.append(self.scrape_company_news(company, config))
        
        # News sources
        tasks.append(self.scrape_news_sources())
        
        # Regulatory sources
        tasks.append(self.scrape_regulatory_news())
        
        # Execute all scraping tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                print(f"Scraping error: {result}")
        
        print(f"Collected {len(all_articles)} articles")
        
        # Process articles
        new_articles_count = 0
        for article in all_articles:
            if not self.is_duplicate(article):
                # Generate summary
                article["summary"] = await self.generate_summary(article)
                
                # Save to database
                self.save_article(article)
                new_articles_count += 1
        
        print(f"Saved {new_articles_count} new articles")

    def get_latest_news(self) -> Dict[str, Any]:
        """Get latest news organized by categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get articles from last 7 days
        cursor.execute('''
            SELECT title, summary, source, category, url, published_date, scraped_date
            FROM articles 
            WHERE scraped_date > datetime('now', '-7 days')
            ORDER BY scraped_date DESC
        ''')
        
        articles = cursor.fetchall()
        conn.close()
        
        # Organize by category
        categorized_news = {
            "Company News": [],
            "Industry News": [],
            "Regulatory": []
        }
        
        for article in articles:
            article_dict = {
                "title": article[0],
                "summary": article[1],
                "source": article[2],
                "category": article[3],
                "url": article[4],
                "published_date": article[5],
                "scraped_date": article[6]
            }
            
            category = article[3]
            if category in categorized_news:
                categorized_news[category].append(article_dict)
        
        return categorized_news

    def parse_rss_content(self, rss_content: str, source: str, category: str) -> List[Dict]:
        """Parse RSS content manually without feedparser"""
        articles = []
        try:
            # Remove XML namespace declarations to simplify parsing
            cleaned_content = re.sub(r'xmlns[^=]*="[^"]*"', '', rss_content)
            root = ET.fromstring(cleaned_content)
            
            # Find all item elements (RSS) or entry elements (Atom)
            items = root.findall('.//item') or root.findall('.//entry')
            
            for item in items[:15]:  # Limit to 15 recent articles
                title_elem = item.find('title')
                description_elem = item.find('description') or item.find('summary') or item.find('content')
                link_elem = item.find('link')
                pubdate_elem = item.find('pubDate') or item.find('published') or item.find('updated')
                
                if title_elem is not None:
                    article = {
                        "title": title_elem.text or "",
                        "content": description_elem.text or "" if description_elem is not None else "",
                        "url": link_elem.text or "" if link_elem is not None else "",
                        "published_date": pubdate_elem.text or "" if pubdate_elem is not None else "",
                        "source": source,
                        "category": category
                    }
                    articles.append(article)
                    
        except ET.ParseError as e:
            print(f"Error parsing RSS for {source}: {e}")
        except Exception as e:
            print(f"Unexpected error parsing RSS for {source}: {e}")
            
        return articles