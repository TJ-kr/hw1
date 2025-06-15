import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import sys

# Gmail API 스코프 설정
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    try:
        # token.pickle 파일이 있으면 토큰 로드
        if os.path.exists('token.pickle'):
            print("Loading existing token...")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # 유효한 인증 정보가 없으면 새로 인증
        if not creds or not creds.valid:
            print("Getting new credentials...")
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("Starting new authentication flow...")
                client_secret_file = '/Users/jean/Cursor ai/client_secret_189541252659-3uop7qui3do2ir73li35l7ui3d76nuav.apps.googleusercontent.com.json'
                print(f"Using client secret file: {client_secret_file}")
                if not os.path.exists(client_secret_file):
                    print(f"Error: Client secret file not found at {client_secret_file}")
                    sys.exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_file,
                    SCOPES)
                print("Running local server for authentication...")
                creds = flow.run_local_server(port=0)
            
            # 토큰 저장
            print("Saving credentials...")
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        print("Building Gmail service...")
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        print(f"Error in get_gmail_service: {str(e)}")
        raise

def create_message(sender, to, subject, message_text):
    try:
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    except Exception as e:
        print(f"Error in create_message: {str(e)}")
        raise

def send_message(service, user_id, message):
    try:
        print("Sending message...")
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as e:
        print(f'Error in send_message: {str(e)}')
        raise

def main():
    try:
        print("Starting email sending process...")
        # 프로젝트 요약 내용
        project_summary = """
안녕하세요,

NewsletterAi 프로젝트 요약 내용입니다:

1. 프로젝트 개요
- AI 기반 뉴스레터 생성 시스템
- 사용자 맞춤형 뉴스 콘텐츠 제공
- 자동화된 이메일 발송 기능

2. 주요 기능
- 뉴스 데이터 수집 및 분석
- AI를 활용한 콘텐츠 생성
- 사용자 맞춤형 뉴스레터 포맷팅
- 자동 이메일 발송

3. 기술 스택
- Python
- Flask
- SQLite
- Google API
- OpenAI API

4. 프로젝트 구조
- app/: 메인 애플리케이션 코드
- templates/: 웹 템플릿
- static/: 정적 파일
- tests/: 테스트 코드
- venv/: 가상환경

5. 설치 및 실행 방법
- requirements.txt의 의존성 설치
- 환경 변수 설정
- Flask 서버 실행

자세한 내용은 GitHub 저장소에서 확인하실 수 있습니다:
https://github.com/TJ-kr/cvc

감사합니다.
"""

        # Gmail 서비스 초기화
        print("Initializing Gmail service...")
        service = get_gmail_service()
        
        # 이메일 메시지 생성
        print("Creating email message...")
        message = create_message(
            'tj456852@gmail.com',
            'tj456852@gmail.com',
            'NewsletterAi 프로젝트 요약',
            project_summary
        )
        
        # 이메일 전송
        print("Sending email...")
        send_message(service, 'me', message)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main() 