from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Article(Base):
    """기사 정보를 저장하는 데이터베이스 모델"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)  # 기사 제목
    content = Column(Text, nullable=False)       # 기사 본문
    url = Column(String(1000), nullable=False)   # 기사 URL
    source = Column(String(100), nullable=False) # 출처 (예: 조선일보, 중앙일보 등)
    published_at = Column(DateTime, nullable=False) # 발행일시
    category = Column(String(50))                # 카테고리 (예: 주식, 부동산, 금융 등)
    importance_score = Column(Float)             # 중요도 점수 (0.0 ~ 1.0)
    summary = Column(Text)                       # AI가 생성한 요약
    created_at = Column(DateTime, default=datetime.utcnow)  # 수집 시간
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 업데이트 시간 