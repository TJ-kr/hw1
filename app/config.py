import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# .env 파일 로드
load_dotenv()

# 데이터베이스 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news.db")

# 뉴스 수집 설정
NEWS_SOURCES = [
    {
        "name": "조선일보",
        "url": "https://www.chosun.com",
        "search_url": "https://search.daum.net/search?w=news&q={keyword}&spacing=0&cluster=n&DA=STC&period=w",
        "type": "news",
        "selectors": {
            "title": "h1.news_title",
            "content": "div.news_body",
            "date": "span.date"
        }
    },
    {
        "name": "중앙일보",
        "url": "https://www.joongang.co.kr",
        "search_url": "https://search.daum.net/search?w=news&q={keyword}&spacing=0&cluster=n&DA=STC&period=w",
        "type": "news",
        "selectors": {
            "title": "h1.headline",
            "content": "div.article_body",
            "date": "span.date"
        }
    },
    {
        "name": "매일경제",
        "url": "https://www.mk.co.kr",
        "search_url": "https://search.daum.net/search?w=news&q={keyword}&spacing=0&cluster=n&DA=STC&period=w",
        "type": "news",
        "selectors": {
            "title": "h2.title",
            "content": "div.news_body",
            "date": "span.date"
        }
    },
    {
        "name": "한국일보",
        "url": "https://www.hankookilbo.com",
        "search_url": "https://search.daum.net/search?w=news&q={keyword}&spacing=0&cluster=n&DA=STC&period=w",
        "type": "news",
        "selectors": {
            "title": "h1.title",
            "content": "div.article_body",
            "date": "span.date"
        }
    },
    {
        "name": "동아일보",
        "url": "https://www.donga.com",
        "search_url": "https://search.daum.net/search?w=news&q={keyword}&spacing=0&cluster=n&DA=STC&period=w",
        "type": "news",
        "selectors": {
            "title": "h1.title",
            "content": "div.article_body",
            "date": "span.date"
        }
    }
]

# 검색 설정
SEARCH_SETTINGS = {
    "max_results": 50,  # 최대 검색 결과 수
    "date_range": 7,    # 최근 일주일
    "min_content_length": 100  # 최소 본문 길이
}

# 분석 설정
CATEGORIES = ["주식", "부동산", "금융", "산업", "국제경제", "정책"]
IMPORTANCE_THRESHOLD = 0.7  # 중요도 점수 임계값 