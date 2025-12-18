from fastapi import FastAPI, Request
import json
import predictor
import repo

app = FastAPI(title="NBA Predictor App", version="1.0")


@app.get("/")
def read_root():
    return {"message": "NBA Predictor App"}

@app.post("/forward")
async def forward(request: Request):
    input = None
    try:
        input = json.loads(await request.body())
    except Exception:
        return {"error": "Invalid JSON"}, 400
    
    try:
        prediction = predictor.get_prediction(input)
    except Exception:
        return {"error": "Failed to get prediction"}, 403

    try:
        repo.add_prediction(str(input), str(prediction))
    except Exception:
        return {"error": "Failed to add prediction"}, 500
    
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
