from typing import Dict, Tuple
import logging
import re
from datetime import datetime
from app.config import CATEGORIES, IMPORTANCE_THRESHOLD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """뉴스 기사를 분석하는 서비스"""
    
    def __init__(self):
        # 카테고리별 키워드 정의
        self.category_keywords = {
            "주식": ["주가", "코스피", "코스닥", "증시", "주식", "투자", "배당"],
            "부동산": ["아파트", "부동산", "집값", "전세", "월세", "매매"],
            "금융": ["은행", "금리", "대출", "예금", "금융", "보험"],
            "산업": ["기업", "산업", "공장", "생산", "수출", "수입"],
            "국제경제": ["달러", "환율", "해외", "글로벌", "국제", "수출"],
            "정책": ["정부", "정책", "법안", "규제", "세금", "지원"]
        }
        
        # 중요도 키워드 정의
        self.importance_keywords = {
            "high": ["긴급", "특보", "단독", "속보", "중요", "대형", "첫"],
            "medium": ["발표", "결정", "예정", "계획", "추진", "검토"],
            "low": ["예상", "전망", "분석", "조사", "연구"]
        }
    
    def analyze_article(self, article: Dict) -> Tuple[float, str, str]:
        """기사를 분석하여 중요도, 카테고리, 요약을 반환합니다."""
        try:
            title = article['title']
            content = article['content']
            
            # 카테고리 분석
            category_scores = {cat: 0 for cat in CATEGORIES}
            for category, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in title or keyword in content:
                        category_scores[category] += 1
            
            category = max(category_scores.items(), key=lambda x: x[1])[0]
            
            # 중요도 분석
            importance_score = 0.0
            for level, keywords in self.importance_keywords.items():
                for keyword in keywords:
                    if keyword in title:
                        if level == "high":
                            importance_score += 0.3
                        elif level == "medium":
                            importance_score += 0.2
                        else:
                            importance_score += 0.1
            
            importance_score = min(1.0, importance_score)
            
            # 요약 생성 (첫 문장 추출)
            sentences = re.split(r'[.!?]+', content)
            summary = sentences[0].strip() if sentences else "요약을 생성할 수 없습니다."
            
            return importance_score, category, summary
            
        except Exception as e:
            logger.error(f"Error analyzing article: {str(e)}")
            return 0.0, "분류불가", "분석 실패"
    
    def is_important(self, importance_score: float) -> bool:
        """중요도 점수가 임계값을 넘는지 확인합니다."""
        return importance_score >= IMPORTANCE_THRESHOLD 