from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import asyncio
from datetime import datetime, timedelta

from app.models.article import Article
from app.utils.database import get_db, init_db
from app.services.scraper import NewsScraper
from app.services.analyzer import NewsAnalyzer

app = FastAPI(title="경제뉴스 AI 에이전트")

# 정적 파일과 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    init_db()

# 웹 인터페이스
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """메인 페이지를 표시합니다."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/search", response_class=HTMLResponse)
async def search_articles(
    request: Request,
    keyword: str,
    db: Session = Depends(get_db)
):
    """키워드로 기사를 검색합니다."""
    try:
        async with NewsScraper() as scraper:
            articles = await scraper.search_articles(keyword)
            
        analyzer = NewsAnalyzer()
        processed_articles = []
        
        for article in articles:
            # 기사 분석
            importance_score, category, summary = analyzer.analyze_article(article)
            
            # 데이터베이스에 저장
            db_article = Article(
                title=article["title"],
                content=article["content"],
                url=article["url"],
                source=article["source"],
                published_at=article["published_at"],
                category=category,
                importance_score=importance_score,
                summary=summary
            )
            db.add(db_article)
            processed_articles.append(db_article)
        
        db.commit()
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "articles": processed_articles,
                "keyword": keyword
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/articles/", response_class=HTMLResponse)
async def list_articles(
    request: Request,
    category: str = None,
    important_only: bool = False,
    db: Session = Depends(get_db)
):
    """기사 목록을 표시합니다."""
    query = db.query(Article)
    
    if category:
        query = query.filter(Article.category == category)
    if important_only:
        query = query.filter(Article.importance_score >= 0.7)
    
    articles = query.order_by(Article.published_at.desc()).all()
    return templates.TemplateResponse(
        "articles.html",
        {
            "request": request,
            "articles": articles,
            "category": category,
            "important_only": important_only
        }
    )

@app.get("/articles/{article_id}", response_class=HTMLResponse)
async def view_article(article_id: int, request: Request, db: Session = Depends(get_db)):
    """특정 기사를 표시합니다."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="기사를 찾을 수 없습니다")
    return templates.TemplateResponse(
        "article.html",
        {"request": request, "article": article}
    )

# 주기적인 뉴스 수집을 위한 스케줄러
@app.on_event("startup")
async def schedule_news_collection():
    """주기적으로 인기 키워드로 뉴스를 수집합니다."""
    popular_keywords = ["주식", "부동산", "금리", "환율"]
    while True:
        try:
            async with NewsScraper() as scraper:
                for keyword in popular_keywords:
                    articles = await scraper.search_articles(keyword)
                    analyzer = NewsAnalyzer()
                    db = next(get_db())
                    
                    for article in articles:
                        importance_score, category, summary = analyzer.analyze_article(article)
                        db_article = Article(
                            title=article["title"],
                            content=article["content"],
                            url=article["url"],
                            source=article["source"],
                            published_at=article["published_at"],
                            category=category,
                            importance_score=importance_score,
                            summary=summary
                        )
                        db.add(db_article)
                    
                    db.commit()
            
            await asyncio.sleep(3600)  # 1시간마다 실행
        except Exception as e:
            logger.error(f"Error in news collection: {str(e)}")
            await asyncio.sleep(300)  # 오류 발생시 5분 후 재시도 