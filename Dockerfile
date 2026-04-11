FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=120

# 배포용은 requirements-docker.txt 사용 (torch/sentence-transformers 제외로 빌드 실패 방지)
COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
 && if pip show torch >/dev/null 2>&1; then echo "ERROR: torch must not be installed (image too large)"; exit 1; fi

# 저장소 전체(COPY .) 대신 실행에 필요한 파일만 — 대용량 데이터·문서가 이미지에 들어가 5GB 제한을 넘지 않도록 함
COPY streamlit_app.py gemini_file_search.py ./

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
