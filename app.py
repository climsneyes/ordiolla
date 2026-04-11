"""
Cloudtype Python 템플릿 기본값은 `gunicorn`(8080 점유) + `app:app` 입니다.
Streamlit도 같은 포트에 바인드할 수 없어, worker에서 exec 로 Streamlit을 띄우는 방식은
「Port 8080 is not available」 로 실패합니다.

해결: Cloudtype 서비스 설정에서「시작 명령」을 Streamlit만 실행하도록 바꾸세요.
(gunicorn이 아니라 streamlit 이 프로세스 1번으로 떠야 합니다.)

이 모듈의 Flask `app` 은 gunicorn이 기본으로 돌 때만 쓰이며,
브라우저에 안내 문구를 보여 줍니다. 시작 명령을 streamlit 으로 바꾸면 이 파일은 사용되지 않습니다.
"""
from __future__ import annotations

from flask import Flask, Response

app = Flask(__name__)

_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Cloudtype — Streamlit 시작 명령 필요</title>
<style>
body{font-family:system-ui,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;line-height:1.5;}
code,pre{background:#f4f4f5;padding:.2rem .4rem;border-radius:4px;display:block;white-space:pre-wrap;word-break:break-all;}
h1{font-size:1.25rem;}
.box{border:1px solid #e4e4e7;border-radius:8px;padding:1rem;margin-top:1rem;background:#fafafa;}
</style>
</head>
<body>
<h1>Streamlit 앱은 gunicorn과 동시에 8080 포트를 쓸 수 없습니다</h1>
<p>Cloudtype 대시보드에서 이 서비스의 <strong>시작 명령(Start Command)</strong>을 아래처럼 바꾼 뒤 <strong>재배포</strong>하세요.</p>
<div class="box">
<pre><code>streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false</code></pre>
</div>
<p>포트 필드는 Cloudtype에 안내된 값(보통 8080)과 맞추면 됩니다. 변경 후에는 gunicorn 대신 Streamlit만 실행됩니다.</p>
</body>
</html>"""


@app.get("/")
def _root() -> Response:
    return Response(_HTML, mimetype="text/html; charset=utf-8")


@app.get("/healthz")
def _healthz() -> tuple[str, int]:
    return "ok", 200
