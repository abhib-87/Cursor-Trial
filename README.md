# Automotive News Aggregator

A comprehensive automotive news aggregation system that collects news from various automotive companies, industry news organizations, and regulatory bodies worldwide. The system provides AI-powered TL;DR summaries, duplicate detection, and a modern web interface.

## Features

### 🚗 **Multi-Source News Collection**
- **Automotive Companies**: Tesla, Ford, GM, Toyota, BMW, Mercedes, Volkswagen
- **Industry News**: Automotive News, Motor Trend, Car and Driver, Autoblog, Reuters, Bloomberg
- **Regulatory Bodies**: NHTSA, IIHS, EPA

### 🤖 **AI-Powered Summarization**
- Uses OpenAI GPT-3.5-turbo for intelligent TL;DR summaries
- Fallback to TextBlob-based summarization if OpenAI API is not available
- Concise 2-3 sentence summaries for quick reading

### 🔍 **Advanced Duplicate Detection**
- Content hash-based exact duplicate detection
- TF-IDF and cosine similarity for near-duplicate detection
- Configurable similarity threshold (default: 0.7)
- Prevents same news from different sources cluttering the feed

### 📅 **Automated Daily Collection**
- Scheduled daily news collection at 6:00 AM
- Background processing with thread-safe operations
- Initial collection on startup
- Manual refresh capability through web interface

### 🎨 **Modern Web Interface**
- Responsive design with mobile support
- Three organized sections: Company News, Industry News, Regulatory News
- Beautiful gradient design with hover effects
- Real-time refresh functionality
- Auto-refresh every 30 minutes

### 💾 **Data Persistence**
- SQLite database for reliable data storage
- Efficient querying with date-based filtering
- Content and similarity hashing for deduplication
- 7-day article retention for optimal performance

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd automotive-news-aggregator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key (optional)
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the web interface:**
   Open your browser and navigate to `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# OpenAI API Key for news summarization (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Database configuration
DATABASE_PATH=news_database.db

# Similarity threshold for duplicate detection (0.0 to 1.0)
SIMILARITY_THRESHOLD=0.7

# Schedule time for daily news collection (24-hour format)
COLLECTION_TIME=06:00

# Web server configuration
HOST=0.0.0.0
PORT=8000
```

### News Sources Configuration

The system is configured to collect from:

**Automotive Companies:**
- Tesla (website scraping)
- Ford (RSS feed)
- GM (RSS feed)
- Toyota (website scraping)
- BMW (website scraping)
- Mercedes (website scraping)
- Volkswagen (website scraping)

**Industry News Sources:**
- Automotive News (RSS)
- Motor Trend (RSS)
- Car and Driver (RSS)
- Autoblog (RSS)
- Reuters Autos (RSS)
- Bloomberg Autos (RSS)

**Regulatory Sources:**
- NHTSA (website scraping)
- IIHS (website scraping)
- EPA (website scraping)

## API Endpoints

### GET `/`
Main web interface displaying categorized automotive news.

### GET `/api/news`
Returns JSON data of latest news organized by categories.

**Response:**
```json
{
  "Company News": [...],
  "Industry News": [...],
  "Regulatory": [...]
}
```

### POST `/api/refresh`
Manually triggers news collection and processing.

**Response:**
```json
{
  "status": "success",
  "message": "News refreshed successfully"
}
```

## Architecture

### Core Components

1. **NewsAggregator** (`news_aggregator.py`)
   - Main class handling news collection, processing, and storage
   - Implements duplicate detection algorithms
   - Manages AI-powered summarization

2. **Scheduler** (`scheduler.py`)
   - Handles daily automated news collection
   - Thread-safe background processing
   - Configurable collection timing

3. **FastAPI Application** (`app.py`)
   - Web server and API endpoints
   - Template rendering for web interface
   - Static file serving

4. **Database Schema**
   - SQLite database with optimized indexing
   - Content and similarity hashing
   - Date-based filtering capabilities

### Duplicate Detection Algorithm

The system uses a two-tier approach for duplicate detection:

1. **Exact Duplicates**: MD5 hash of article content
2. **Similar Articles**: TF-IDF vectorization + cosine similarity

This ensures that the same news story published by different sources is only shown once.

### Summarization Process

1. **Primary**: OpenAI GPT-3.5-turbo with automotive-specific prompts
2. **Fallback**: TextBlob sentence extraction for basic summarization
3. **Length**: Optimized for 2-3 sentences (150 tokens max)

## Usage

### Daily Operation
The system automatically:
1. Collects news from all configured sources at 6:00 AM daily
2. Processes and deduplicates articles
3. Generates AI summaries
4. Stores new articles in the database
5. Serves updated content through the web interface

### Manual Operations
- **Refresh News**: Click the "Refresh News" button on the web interface
- **API Access**: Use `/api/news` endpoint for programmatic access
- **Database Access**: Direct SQLite access for advanced queries

### Monitoring
- Check console logs for collection status
- Monitor database size and performance
- Review error logs for failed scraping attempts

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - System falls back to TextBlob summarization
   - Check API key configuration in `.env`

2. **Website Scraping Failures**
   - Some sites may block automated requests
   - RSS feeds are more reliable than direct scraping

3. **Database Lock Errors**
   - Ensure only one instance is running
   - Check file permissions for database file

4. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

### Performance Optimization

- **Database**: Regular cleanup of old articles (>7 days)
- **Memory**: Monitor RSS feed parsing for large feeds
- **Network**: Implement request timeouts and retries
- **Caching**: Consider Redis for high-traffic scenarios

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new news sources or improve existing functionality
4. Test thoroughly with various scenarios
5. Submit a pull request

### Adding New News Sources

To add a new automotive news source:

1. Add to the appropriate dictionary in `news_aggregator.py`
2. Implement source-specific parsing logic
3. Test duplicate detection with existing articles
4. Update documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and personal use. Please respect the terms of service of all news sources and consider implementing appropriate rate limiting and caching mechanisms for production use.
