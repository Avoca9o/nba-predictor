from fastapi import FastAPI

app = FastAPI(title="NBA Predictor App", version="1.0")

@app.get("/")
def read_root():
    return {"message": "NBA Predictor App"}
