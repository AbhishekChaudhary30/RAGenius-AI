from fastapi import FastAPI

app = FastAPI(
  title = "RAGenius AI",
  version = "1.0.0",
)

@app.get("/")
def home():
  return {
    "application":"RAGenius AI",
    "status":"Running",
  }