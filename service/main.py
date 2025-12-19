from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
import predictor
import repo
import auth
import config

app = FastAPI(title="NBA Predictor App", version="1.0")


@app.on_event("startup")
async def startup_event():
    if not repo.has_admin():
        if config.ADMIN_PASSWORD:
            try:
                repo.create_user(
                    username=config.ADMIN_USERNAME,
                    password=config.ADMIN_PASSWORD,
                    role='admin'
                )
                print(f'Default admin "{config.ADMIN_USERNAME}" created successfully')
            except Exception as e:
                print(f'Failed to create default admin: {e}')
        else:
            print('Warning: No admin found and ADMIN_PASSWORD not set. Please create admin manually.')

class TokenRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "NBA Predictor App"}


@app.post("/token")
async def login(token_request: TokenRequest):
    user = repo.get_user_by_username(token_request.username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    if not repo.verify_password(token_request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role},
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
