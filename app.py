"""
Cloudtype Python 템플릿은 기본으로 `gunicorn ... app:app` 을 실행합니다.
Streamlit은 WSGI 앱이 아니므로, worker가 `app` 모듈을 로드하는 순간
이 프로세스를 `streamlit run` 으로 바꿉니다.

더 깔끔한 방법: Cloudtype 서비스 설정의「시작 명령」을 아래로 바꾸면 gunicorn 없이 Streamlit만 실행됩니다.
  streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

(워커가 여러 개면 같은 PORT 로 충돌할 수 있어, 시작 명령 방식이 더 안전합니다.)
"""
from __future__ import annotations

import os
import sys


def app(environ, start_response):
    """gunicorn이 import 시점에 callable을 찾을 수 있도록 하는 더미 WSGI. exec 이후에는 사용되지 않습니다."""
    start_response("500 Internal Server Error", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Unreachable: process should have been replaced by Streamlit."]


def _exec_streamlit() -> None:
    port = os.environ.get("PORT", "8080")
    argv = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.port",
        port,
        "--server.address",
        "0.0.0.0",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    os.execv(sys.executable, argv)


_exec_streamlit()
