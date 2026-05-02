from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.v1 import api_router
from app.core.exceptions import DomainError

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


app.include_router(api_router, prefix="/api/v1")


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
