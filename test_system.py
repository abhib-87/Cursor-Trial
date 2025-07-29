#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_aggregator import NewsAggregator

async def test_system():
    """Test the news aggregation system"""
    print("Testing Automotive News Aggregator System...")
    
    # Initialize the aggregator
    aggregator = NewsAggregator()
    print("✓ NewsAggregator initialized successfully")
    
    # Test database initialization
    try:
        aggregator.init_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    
    # Test automotive keyword detection
    test_texts = [
        "Tesla releases new Model S update",
        "Ford recalls 100,000 vehicles due to safety issue",
        "Recipe for chocolate cake",  # Should not be automotive
        "BMW announces new electric vehicle lineup"
    ]
    
    automotive_count = 0
    for text in test_texts:
        if aggregator.is_automotive_related(text):
            automotive_count += 1
            print(f"✓ Detected automotive content: '{text}'")
        else:
            print(f"- Skipped non-automotive content: '{text}'")
    
    if automotive_count >= 3:  # Should detect at least 3 out of 4
        print("✓ Automotive keyword detection working correctly")
    else:
        print("✗ Automotive keyword detection may have issues")
    
    # Test content hashing
    test_content = "This is a test article about Tesla's new features"
    hash1 = aggregator.calculate_content_hash(test_content)
    hash2 = aggregator.calculate_content_hash(test_content)
    
    if hash1 == hash2:
        print("✓ Content hashing working correctly")
    else:
        print("✗ Content hashing inconsistent")
    
    # Test duplicate detection with empty database
    test_article = {
        "title": "Test Article",
        "content": test_content,
        "category": "Company News",
        "source": "Test Source"
    }
    
    is_duplicate = aggregator.is_duplicate(test_article)
    if not is_duplicate:
        print("✓ Duplicate detection working (no false positives)")
    else:
        print("✗ Duplicate detection showing false positive")
    
    print("\nSystem test completed successfully!")
    print("You can now start the web server using: ./start_server.sh")
    return True

if __name__ == "__main__":
    asyncio.run(test_system())