from fastapi import FastAPI

app = FastAPI(
    title="Bond Intelligence PoC",
    version="0.1.0",
)

@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}