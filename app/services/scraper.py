import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import re
from urllib.parse import quote

from app.config import NEWS_SOURCES, SEARCH_SETTINGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    """뉴스 기사를 수집하는 스크래퍼"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str) -> str:
        """웹 페이지를 가져옵니다."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Error fetching {url}: Status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
    
    def parse_article(self, html: str, source: Dict) -> Dict:
        """HTML에서 기사 정보를 추출합니다."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            selectors = source["selectors"]
            
            # 제목 추출
            title_elem = soup.select_one(selectors["title"])
            title = title_elem.text.strip() if title_elem else "제목을 찾을 수 없습니다"
            
            # 본문 추출
            content_elem = soup.select_one(selectors["content"])
            content = content_elem.text.strip() if content_elem else "내용을 찾을 수 없습니다"
            
            # 날짜 추출
            date_elem = soup.select_one(selectors["date"])
            date_str = date_elem.text.strip() if date_elem else datetime.now().strftime("%Y.%m.%d %H:%M")
            
            # 날짜 형식 변환
            try:
                if "년" in date_str:
                    # 한글 날짜 형식 변환 (예: 2024년 3월 15일)
                    date_str = re.sub(r'(\d+)년\s*(\d+)월\s*(\d+)일', r'\1.\2.\3', date_str)
                published_at = datetime.strptime(date_str, '%Y.%m.%d %H:%M')
            except ValueError:
                published_at = datetime.now()
            
            return {
                "title": title,
                "content": content,
                "published_at": published_at,
                "source": source["name"]
            }
        except Exception as e:
            logger.error(f"Error parsing article from {source['name']}: {str(e)}")
            return None
    
    async def search_articles(self, keyword: str) -> List[Dict]:
        """키워드로 기사를 검색합니다."""
        articles = []
        seen_urls = set()  # 중복 URL 체크를 위한 set
        
        for source in NEWS_SOURCES:
            try:
                # 검색 URL 생성
                search_url = source["search_url"].format(keyword=quote(keyword))
                html = await self.fetch_page(search_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    # 검색 결과에서 기사 링크 추출
                    article_links = soup.select("a.f_link_b")
                    
                    for link in article_links[:SEARCH_SETTINGS["max_results"]]:
                        article_url = link.get("href")
                        
                        # 중복 체크
                        if article_url in seen_urls:
                            continue
                        seen_urls.add(article_url)
                        
                        # 기사 페이지 가져오기
                        article_html = await self.fetch_page(article_url)
                        if article_html:
                            article = self.parse_article(article_html, source)
                            if article:
                                # 최근 일주일 기사만 포함
                                if datetime.now() - article["published_at"] <= timedelta(days=SEARCH_SETTINGS["date_range"]):
                                    article["url"] = article_url
                                    articles.append(article)
            
            except Exception as e:
                logger.error(f"Error searching articles from {source['name']}: {str(e)}")
        
        # 날짜순으로 정렬
        articles.sort(key=lambda x: x["published_at"], reverse=True)
        return articles 