from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
import predictor
import repo
import auth

app = FastAPI(title="NBA Predictor App", version="1.0")

class TokenRequest(BaseModel):
    username: str
    role: str

@app.get("/")
def read_root():
    return {"message": "NBA Predictor App"}


@app.post("/token")
async def login(token_request: TokenRequest):
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": token_request.username, "role": token_request.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
async def history(current_admin: auth.TokenData = Depends(auth.get_current_admin)):
    try:
        predictions = repo.get_predictions()
    except Exception:
        return {"error": "Failed to get predictions"}, 500
    
    return {"predictions": [str(prediction) for prediction in predictions]}

@app.delete("/history")
async def delete_history(current_admin: auth.TokenData = Depends(auth.get_current_admin)):
    try:
        repo.delete_predictions()
    except Exception:
        return {"error": "Failed to delete predictions"}, 500
    return {"message": "Predictions deleted"}

@app.get("/stats")
async def stats(current_admin: auth.TokenData = Depends(auth.get_current_admin)):
    return {"message": "Not implemented"}
