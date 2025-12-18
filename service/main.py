from fastapi import FastAPI, Request, HTTPException
import predictor
import repo

app = FastAPI(title="NBA Predictor App", version="1.0")

@app.get("/")
def read_root():
    return {"message": "NBA Predictor App"}

@app.post("/forward")
async def forward(request: Request):
    body = None
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    try:
        prediction = predictor.get_prediction(body)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Failed to get prediction: {e}")

    try:
        repo.add_prediction(str(body), str(prediction))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add prediction")

    return {"prediction": prediction}

@app.get("/history")
async def history():
    try:
        predictions = repo.get_predictions()
    except Exception:
        return {"error": "Failed to get predictions"}, 500
    
    return {"predictions": [str(prediction) for prediction in predictions]}

@app.delete("/history")
async def delete_history():
    # TODO: Implement logic with key or token
    try:
        repo.delete_predictions()
    except Exception:
        return {"error": "Failed to delete predictions"}, 500
    return {"message": "Predictions deleted"}

@app.get("/stats")
async def stats():
    return {"message": "Not implemented"}
