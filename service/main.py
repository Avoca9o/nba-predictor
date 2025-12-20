from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
import predictor
import repo
import auth
import config
import stats_collector
import time

app = FastAPI(title="NBA Predictor App", version="1.0")
time_collector = stats_collector.DurationStorage()
req_collector = stats_collector.RequestsStorage()

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
    start_time = time.perf_counter()
    body = None
    try:
        body = await request.json()
    except Exception:
        time_collector.add(time.perf_counter() - start_time)
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    req_collector.add(len(str(body)))

    try:
        prediction = predictor.get_prediction(body)
    except Exception as e:
        time_collector.add(time.perf_counter() - start_time)
        raise HTTPException(status_code=403, detail=f"Failed to get prediction: {e}")

    try:
        repo.add_prediction(str(body), str(prediction))
    except Exception:
        time_collector.add(time.perf_counter() - start_time)
        raise HTTPException(status_code=500, detail="Failed to add prediction")

    time_collector.add(time.perf_counter() - start_time)
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
    return {
        "mean": f"{time_collector.get_mean():.6f}s",
        "50 quantile": f"{time_collector.get_percentile(50):.6f}s",
        "95 quantile": f"{time_collector.get_percentile(95):.6f}s",
        "99 quantile": f"{time_collector.get_percentile(99):.6f}s",
        "mena req length": req_collector.get_req_data()
    }