from fastapi import FastAPI

app = FastAPI(title="FastAPI Todolist")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "OKcho"}
