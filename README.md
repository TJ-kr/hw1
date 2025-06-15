# 경제기사 수집 AI 에이전트

자동으로 인터넷에서 경제 관련 뉴스를 수집하고 분석하는 AI 에이전트입니다.

## 주요 기능
- 경제 뉴스 자동 수집
- AI를 통한 기사 분석 및 분류
- 중요 뉴스 실시간 모니터링
- REST API를 통한 데이터 접근

## 설치 방법
1. 저장소 클론
```bash
git clone [repository-url]
cd [repository-name]
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가:
```
OPENAI_API_KEY=your_api_key_here
```

## 실행 방법
```bash
uvicorn app.main:app --reload
```

## API 문서
서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조
```
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
├── .env
├── requirements.txt
└── README.md
``` 