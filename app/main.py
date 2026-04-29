from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head><title>Todolist</title></head>
        <body>
            <h1>Todolist API is running</h1>
            <button onclick="fetch('/health').then(r=>r.json()).then(d=>alert(d.status))">
                Check Health
            </button>
        </body>
    </html>
    """


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}
